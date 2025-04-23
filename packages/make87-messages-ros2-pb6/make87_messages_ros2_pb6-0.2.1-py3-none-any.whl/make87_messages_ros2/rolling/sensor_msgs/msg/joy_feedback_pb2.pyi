from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class JoyFeedback(_message.Message):
    __slots__ = ("type", "id", "intensity")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    INTENSITY_FIELD_NUMBER: _ClassVar[int]
    type: int
    id: int
    intensity: float
    def __init__(self, type: _Optional[int] = ..., id: _Optional[int] = ..., intensity: _Optional[float] = ...) -> None: ...
