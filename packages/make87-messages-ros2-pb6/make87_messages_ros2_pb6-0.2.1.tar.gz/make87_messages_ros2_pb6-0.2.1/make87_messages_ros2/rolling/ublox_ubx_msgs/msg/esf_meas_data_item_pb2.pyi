from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ESFMeasDataItem(_message.Message):
    __slots__ = ("data_field", "data_type")
    DATA_FIELD_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    data_field: int
    data_type: int
    def __init__(self, data_field: _Optional[int] = ..., data_type: _Optional[int] = ...) -> None: ...
