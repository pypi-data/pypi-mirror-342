from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DataPoint(_message.Message):
    __slots__ = ("name_index", "stamp", "value")
    NAME_INDEX_FIELD_NUMBER: _ClassVar[int]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    name_index: int
    stamp: float
    value: float
    def __init__(self, name_index: _Optional[int] = ..., stamp: _Optional[float] = ..., value: _Optional[float] = ...) -> None: ...
