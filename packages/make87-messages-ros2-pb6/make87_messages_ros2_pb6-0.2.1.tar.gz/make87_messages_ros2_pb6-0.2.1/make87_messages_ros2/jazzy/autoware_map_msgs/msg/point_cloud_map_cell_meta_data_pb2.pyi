from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PointCloudMapCellMetaData(_message.Message):
    __slots__ = ("min_x", "min_y", "max_x", "max_y")
    MIN_X_FIELD_NUMBER: _ClassVar[int]
    MIN_Y_FIELD_NUMBER: _ClassVar[int]
    MAX_X_FIELD_NUMBER: _ClassVar[int]
    MAX_Y_FIELD_NUMBER: _ClassVar[int]
    min_x: float
    min_y: float
    max_x: float
    max_y: float
    def __init__(self, min_x: _Optional[float] = ..., min_y: _Optional[float] = ..., max_x: _Optional[float] = ..., max_y: _Optional[float] = ...) -> None: ...
