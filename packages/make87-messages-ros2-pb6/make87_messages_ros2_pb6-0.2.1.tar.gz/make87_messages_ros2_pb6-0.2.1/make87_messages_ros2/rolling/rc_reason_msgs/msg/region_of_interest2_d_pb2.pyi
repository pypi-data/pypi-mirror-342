from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RegionOfInterest2D(_message.Message):
    __slots__ = ("id", "offset_x", "offset_y", "width", "height")
    ID_FIELD_NUMBER: _ClassVar[int]
    OFFSET_X_FIELD_NUMBER: _ClassVar[int]
    OFFSET_Y_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    id: str
    offset_x: int
    offset_y: int
    width: int
    height: int
    def __init__(self, id: _Optional[str] = ..., offset_x: _Optional[int] = ..., offset_y: _Optional[int] = ..., width: _Optional[int] = ..., height: _Optional[int] = ...) -> None: ...
