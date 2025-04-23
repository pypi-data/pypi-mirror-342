import datetime
import os
import requests
import urllib.parse
import traceback

from .models import LogSeverity, OdysseusLog, OdysseusEvent

from threading import Lock, Timer
from typing import Optional, Any, TypeVar, Generic, Dict
from tzlocal import get_localzone
from uuid import uuid4, UUID

########################################################################################################################
log_silent = False
log_tag = 'Odysseus'

def internal_log(message: str):
    if log_silent:
        return
    ts = datetime.datetime.now(tz=get_localzone())
    time = "{:02d}:{:02d}:{:02d}".format(ts.hour, ts.minute, ts.second)
    print(f"[{time}] [INFO] {log_tag}: {message}")


T = TypeVar('T')

class OdysseusCollection(Generic[T]):

    def __init__(self, endpoint: str, entity_name: str, delay: int = 5):
        self.entries: [T] = []
        self.to_upload: [T] = []
        self.endpoint = endpoint
        self.entity_name = entity_name
        self.delay = delay
        self.timer = None
        self.lock = Lock()

    def add(self, item: T):
        with self.lock:
            self.entries.append(item)

            if self.timer is None:
                self.timer = Timer(self.delay, self.execute_upload)
                self.timer.start()

    def execute_upload(self):

        # copy the entries aside and try to upload them
        with self.lock:
            self.to_upload = self.entries
            self.entries = []

        try:
            success = self.upload_entries(self.to_upload)
            # once upload finished successfully, clear all temporary data
            with self.lock:
                if not success:
                    self.entries = self.to_upload + self.entries
                self.to_upload = []
                self.timer = None
        except Exception as e:
            internal_log(f"Failed to upload {self.entity_name} to Odysseus: {e}")
            with self.lock:
                self.entries = self.to_upload + self.entries
                self.to_upload = []
                self.timer = None

        # restart the timer, if still something awaits sending
        if len(self.entries) > 0:
            with self.lock:
                self.timer = Timer(self.delay, self.execute_upload)
                self.timer.start()

    def upload_entries(self, data: [T]) -> bool:
        url = "https://odysseus.codetitans.dev" + self.endpoint
        response = requests.post(url, json=[x.to_dict() for x in data])

        global log_silent
        if 200 <= response.status_code < 300:
            if not log_silent:
                text = response.text
                internal_log(f"Successfully uploaded {self.entity_name} to Odysseus: {response.status_code} (\"{text}\")")
            return True
        else:
            if not log_silent:
                text = response.text
                internal_log(f"Failed to upload {self.entity_name} to Odysseus: {response.status_code} (\"{text}\")")
            return False


class OdysseusClient:

    def __init__(self, app_id: str, app_key: str, user: Optional[str] = None, session: Optional[UUID] = None,
                 min_severity: LogSeverity = LogSeverity.DEBUG, platform: Optional[int] = None, silent: bool = False,
                 auto_traceback: bool = True, strip_file_name: bool = True):
        global log_silent
        log_silent = silent

        self.user_id = user
        self.session_id = uuid4() if session is None else session
        self.min_severity_level = min_severity
        self.platform = platform
        self.auto_traceback = auto_traceback
        self.strip_file_name = strip_file_name
        self.app_id = app_id
        self.app_key = app_key
        self.logs = OdysseusCollection[OdysseusLog](endpoint="/api/logs" + urllib.parse.quote('/' + app_id + '/' + app_key), delay=5, entity_name="logs")
        self.events = OdysseusCollection[OdysseusEvent](endpoint="/api/events" + urllib.parse.quote('/' + app_id + '/' + app_key), delay=5, entity_name="events")

        internal_log(f"Initialised for application: \"{self.app_id}\" (session: \"{self.session_id.hex}\", delay: {self.logs.delay}s)")

    @property
    def user(self) -> Optional[str]:
        return self.user_id

    @user.setter
    def user(self, value: Optional[str] = None):
        self.user_id = value

    @property
    def session(self) -> UUID:
        return self.session_id

    @session.setter
    def session(self, value: UUID):
        self.session_id = value

    @property
    def min_severity(self) -> LogSeverity:
        return self.min_severity_level

    @min_severity.setter
    def min_severity(self, value: LogSeverity):
        self.min_severity_level = value

    def log(self, message: str, severity: LogSeverity, tag: Optional[str] = None,
            file: Optional[str] = None, method: Optional[str] = None, line: Optional[int] = None, timestamp: Optional[datetime.datetime] = None,
            context: Optional[Dict[str, Any]] = None) -> Optional[OdysseusLog]:

        if severity.value < self.min_severity_level.value:
            return None

        if self.auto_traceback and file is None and method is None and line is None:
            stack = traceback.extract_stack()
            if len(stack) > 2:
                stb = traceback.extract_stack()[-2]
                file = stb.filename
                method = stb.name
                line = stb.lineno

        if self.strip_file_name and file is not None:
            file = os.path.basename(file)

        return self.add_log(OdysseusLog(message, self.session_id, severity=severity, tag=tag, platform=self.platform,
                                        user=self.user_id, timestamp=timestamp,
                                        file=file, method=method, line=line, context=context))

    def add_log(self, entry: OdysseusLog) -> Optional[OdysseusLog]:
        if entry.severity.value < self.min_severity_level.value:
            return None

        self.logs.add(entry)
        return entry

    def event(self, name: str, id: Optional[UUID] = None, type: int = 0, stream_id: Optional[UUID] = None, position: Optional[int] = None,
              timestamp: Optional[datetime.datetime] = None,
              data: Optional[Dict[str, Any]] = None, meta: Optional[Dict[str, Any]] = None) -> OdysseusEvent:
        return self.add_event(OdysseusEvent(
            uuid4() if id is None else id,
            name=name, session_id=self.session_id, type=type, stream_id=stream_id, position=position,
            platform=self.platform, user=self.user, timestamp=timestamp, data=data, meta=meta))

    def add_event(self, event: OdysseusEvent) -> OdysseusEvent:
        self.events.add(event)
        return event




