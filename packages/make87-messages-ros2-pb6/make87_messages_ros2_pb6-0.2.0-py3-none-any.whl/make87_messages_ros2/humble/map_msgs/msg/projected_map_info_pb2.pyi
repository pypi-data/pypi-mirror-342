from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProjectedMapInfo(_message.Message):
    __slots__ = ("header", "frame_id", "x", "y", "width", "height", "min_z", "max_z")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FRAME_ID_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    MIN_Z_FIELD_NUMBER: _ClassVar[int]
    MAX_Z_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    frame_id: str
    x: float
    y: float
    width: float
    height: float
    min_z: float
    max_z: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., frame_id: _Optional[str] = ..., x: _Optional[float] = ..., y: _Optional[float] = ..., width: _Optional[float] = ..., height: _Optional[float] = ..., min_z: _Optional[float] = ..., max_z: _Optional[float] = ...) -> None: ...
