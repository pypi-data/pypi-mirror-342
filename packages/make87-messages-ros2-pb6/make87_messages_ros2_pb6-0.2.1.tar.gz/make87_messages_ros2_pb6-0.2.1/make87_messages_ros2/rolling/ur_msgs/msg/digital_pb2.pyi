from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Digital(_message.Message):
    __slots__ = ("pin", "state")
    PIN_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    pin: int
    state: bool
    def __init__(self, pin: _Optional[int] = ..., state: bool = ...) -> None: ...
