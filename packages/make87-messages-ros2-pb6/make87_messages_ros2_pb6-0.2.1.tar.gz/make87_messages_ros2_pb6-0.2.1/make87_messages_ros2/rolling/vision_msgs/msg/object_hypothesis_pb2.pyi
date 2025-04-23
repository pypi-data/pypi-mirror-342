from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ObjectHypothesis(_message.Message):
    __slots__ = ("class_id", "score")
    CLASS_ID_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    class_id: str
    score: float
    def __init__(self, class_id: _Optional[str] = ..., score: _Optional[float] = ...) -> None: ...
