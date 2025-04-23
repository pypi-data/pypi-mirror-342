from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LaneletMapCellMetaData(_message.Message):
    __slots__ = ("cell_id", "min_x", "max_x", "min_y", "max_y")
    CELL_ID_FIELD_NUMBER: _ClassVar[int]
    MIN_X_FIELD_NUMBER: _ClassVar[int]
    MAX_X_FIELD_NUMBER: _ClassVar[int]
    MIN_Y_FIELD_NUMBER: _ClassVar[int]
    MAX_Y_FIELD_NUMBER: _ClassVar[int]
    cell_id: str
    min_x: float
    max_x: float
    min_y: float
    max_y: float
    def __init__(self, cell_id: _Optional[str] = ..., min_x: _Optional[float] = ..., max_x: _Optional[float] = ..., min_y: _Optional[float] = ..., max_y: _Optional[float] = ...) -> None: ...
