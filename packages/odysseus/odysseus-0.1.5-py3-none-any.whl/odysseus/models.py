import datetime
from enum import IntEnum
from typing import Optional, Dict, Any
from uuid import UUID, uuid4

from tzlocal import get_localzone


class LogSeverity(IntEnum):
    TRACE = 0
    DEBUG = 1
    INFO = 2
    SUCCESS = 3
    WARN = 4
    ERROR = 5
    CRITICAL = 6

class OdysseusLog:

    def __init__(self, message: str, session_id: UUID,
                 severity: LogSeverity = LogSeverity.TRACE, tag: Optional[str] = None, platform: Optional[int] = None,
                 file: Optional[str] = None, method: Optional[str] = None, line: Optional[int] = None,
                 user: Optional[str] = None, timestamp: Optional[datetime.datetime] = None,
                 context: Optional[Dict[str, Any]] = None):

        self.session_id = session_id.hex
        self.message = message
        self.severity = severity
        self.tag = tag
        self.platform = platform
        self.timestamp = datetime.datetime.now(tz=get_localzone()).isoformat() if timestamp is None else timestamp.isoformat()
        self.file = file
        self.method = method
        self.line = line
        self.user = user
        self.context = context

    def to_dict(self):
        result = {'session_id': self.session_id, 'message': self.message, 'severity': self.severity.value, 'timestamp': self.timestamp}
        if self.tag is not None:
            result['tag'] = self.tag
        if self.platform is not None:
            result['platform'] = self.platform
        if self.file is not None:
            result['file'] = self.file
        if self.method is not None:
            result['method'] = self.method
        if self.line is not None:
            result['line'] = self.line
        if self.user is not None:
            result['user'] = self.user
        if self.context is not None:
            result['context'] = self.context
        return result


class OdysseusEvent:

    def __init__(self, id: UUID, name: str, session_id: UUID, type: int = 0,
                 stream_id: Optional[UUID] = None, position: int = 0,
                 platform: Optional[int] = None, user: Optional[str] = None, timestamp: Optional[datetime.datetime] = None,
                 data: Optional[Dict[str, Any]] = None, meta: Optional[Dict[str, Any]] = None):

        self.id = id.hex
        self.session_id = session_id.hex
        self.name = name
        self.type = type
        self.timestamp = datetime.datetime.now(tz=get_localzone()).isoformat() if timestamp is None else timestamp.isoformat()
        self.stream_id = uuid4().hex if stream_id is None else stream_id.hex
        self.position = position
        self.platform = platform
        self.user = user
        self.data = data
        self.meta = meta

    def to_dict(self):
        result = {'id': self.id, 'name': self.name, 'session_id': self.session_id, 'type': self.type,
                  'timestamp': self.timestamp, 'stream_id': self.stream_id, 'position': self.position}
        if self.platform is not None:
            result['platform'] = self.platform
        if self.user is not None:
            result['user'] = self.user
        if self.data is not None:
            result['data'] = self.data
        if self.meta is not None:
            result['meta'] = self.meta
        return result
