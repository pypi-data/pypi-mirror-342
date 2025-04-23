from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CfgANT(_message.Message):
    __slots__ = ("flags", "pins")
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    PINS_FIELD_NUMBER: _ClassVar[int]
    flags: int
    pins: int
    def __init__(self, flags: _Optional[int] = ..., pins: _Optional[int] = ...) -> None: ...
