from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AgentState(_message.Message):
    __slots__ = ("temp", "battery")
    TEMP_FIELD_NUMBER: _ClassVar[int]
    BATTERY_FIELD_NUMBER: _ClassVar[int]
    temp: float
    battery: float
    def __init__(self, temp: _Optional[float] = ..., battery: _Optional[float] = ...) -> None: ...
