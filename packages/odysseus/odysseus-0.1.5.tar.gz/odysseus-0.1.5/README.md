# Odysseus Platform - Python client

This repository contains full source code of the simple Python project capable of uploading log entries or events happening on a backend application - back to the [Odysseus Logging Platform](https://odysseus.codetitans.dev).

Once it's added as a dependency of your Python application, it has to be connected with your existing logging system and logs serialization has to be redirected to be able to process them and pass back to the server.

Official home of this package on [pypi.org](https://pypi.org/project/odysseus/) is [Odysseus Client](https://pypi.org/project/odysseus/).

## Disclaimer

Full utilization of the Odysseus Logging Platform services is subject to the proper contract and not part of that client functionality. By using this software you essentially agree that since it's an open-source project you read it and understand all repercussions of using it. Thus you will never claim or call for any compensations or damages in connection with downtime of your own services caused by this software.

## Logging Levels

In general all parameters exposed by the library are self-explanatory. The only one that could potentially be a source of questions is the `log level`.
Here are the values then expected with a proper meaning (originally based on [ASP.NET Log Levels](https://learn.microsoft.com/en-us/dotnet/api/microsoft.extensions.logging.loglevel?view=net-9.0-pp#fields))

| Value | Name | Description |
| --- | --- | --- |
| 0 | Trace | Lowest level, should be used only during development, cause it can potentially print some sensitive info. |
| 1 | Debug | Typical debugging information with detailed information. |
| 2 | Info | Mid-level debugging, just general information about activity |
| 3 | Success | Mid-level debugging, just successful information about activity |
| 4 | Warn | Logs that describe unexpected and abnormal behavior, potentially some unexpected behaviors happening on other components. |
| 5 | Error | All kids of errors that prevent the application to continue its operation. |
| 6 | Critical | Logs of unrecoverable behaviors of the application, including crashes, lack of local disc-space and everything that requires immediate attention of the administrator. |

## Usage

It's extremely easy to integrate CodeTitans Odysseus Client package with your own project. The client being part of this package has only a single capability to upload any logs entries or custom events back to the backend and correctly identify them online. Follow these 3 simple steps to complete the setup:

1. Install this package into your current environment:

    ```shell
    $ python3 -m pip odysseus
    ```

1. Inside your project import the client class inside your own logging part of the application.

    ```python
    from odysseus import OdysseusClient
    ```

1. Initialize the client with proper credentials, that were given to you, when registered your backend service at [Odysseus Logging Platform](https://odysseus.codetitans.dev)

    ```python
    # ...
    # assuming here is your own logging system that captures activities across the whole application
    # initialize the client with received credentials

    odysseus = OdysseusClient(app_id='app_XXX', app_key='<key>')
    ```

1. Potentially highjack the logging function

    ```python
    def log_entry(level: LogLevel, tag: str, message: str) -> LogEntry:

        # ... other application code removed for clarity ...
        odysseus.log(message=message, severity=LogSeverity(level.value), tag=tag, timestamp=datetime.now(tz=timezone.utc))
    ```

    also add a helper method for sending events:

    ```python
    def log_event(name: str, data: Optional[Dict[str, Any]] = None, type: int = 0,
                  stream_id: Optional[UUID] = None, position: Optional[int] = None, meta: Optional[Dict[str, Any]] = None):
        odysseus.event(name=name, data=data, type=type, stream_id=stream_id, position=position, meta=meta)
    ```

## Examples

As described in the chapter above, usage of this logging client would be as easy as calling the two helper functions:

```python

# log regular message
log_entry(LogLevel.DEBUG, __tag, 'Invoking presentation request')

# or logging an event
log_event('invoicing-started', {'requested-for': company.id, 'ref': order.id, 'amount': order.sum_netto})

```

-----
CodeTitans Sp. z o.o. (2025-)
