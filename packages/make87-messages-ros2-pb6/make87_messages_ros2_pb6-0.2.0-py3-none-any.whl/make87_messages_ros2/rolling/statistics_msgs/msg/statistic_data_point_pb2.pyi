from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class StatisticDataPoint(_message.Message):
    __slots__ = ("data_type", "data")
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    data_type: int
    data: float
    def __init__(self, data_type: _Optional[int] = ..., data: _Optional[float] = ...) -> None: ...
