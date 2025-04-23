from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ConfigLoggerRequest(_message.Message):
    __slots__ = ("logger_name", "level")
    LOGGER_NAME_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    logger_name: str
    level: str
    def __init__(self, logger_name: _Optional[str] = ..., level: _Optional[str] = ...) -> None: ...

class ConfigLoggerResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
