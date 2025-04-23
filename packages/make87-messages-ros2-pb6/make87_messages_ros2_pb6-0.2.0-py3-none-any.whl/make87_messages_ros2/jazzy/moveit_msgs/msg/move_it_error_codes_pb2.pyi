from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class MoveItErrorCodes(_message.Message):
    __slots__ = ("val", "message", "source")
    VAL_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    val: int
    message: str
    source: str
    def __init__(self, val: _Optional[int] = ..., message: _Optional[str] = ..., source: _Optional[str] = ...) -> None: ...
