from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class UniversalJointPos(_message.Message):
    __slots__ = ("name", "ax1", "ax2")
    NAME_FIELD_NUMBER: _ClassVar[int]
    AX1_FIELD_NUMBER: _ClassVar[int]
    AX2_FIELD_NUMBER: _ClassVar[int]
    name: str
    ax1: float
    ax2: float
    def __init__(self, name: _Optional[str] = ..., ax1: _Optional[float] = ..., ax2: _Optional[float] = ...) -> None: ...
