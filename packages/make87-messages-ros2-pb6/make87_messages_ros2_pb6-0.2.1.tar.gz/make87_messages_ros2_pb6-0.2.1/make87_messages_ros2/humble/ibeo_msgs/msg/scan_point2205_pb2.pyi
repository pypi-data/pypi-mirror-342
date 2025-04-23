from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScanPoint2205(_message.Message):
    __slots__ = ("header", "x_position", "y_position", "z_position", "echo_width", "device_id", "layer", "echo", "time_offset", "ground", "dirt", "precipitation", "transparent")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    X_POSITION_FIELD_NUMBER: _ClassVar[int]
    Y_POSITION_FIELD_NUMBER: _ClassVar[int]
    Z_POSITION_FIELD_NUMBER: _ClassVar[int]
    ECHO_WIDTH_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    ECHO_FIELD_NUMBER: _ClassVar[int]
    TIME_OFFSET_FIELD_NUMBER: _ClassVar[int]
    GROUND_FIELD_NUMBER: _ClassVar[int]
    DIRT_FIELD_NUMBER: _ClassVar[int]
    PRECIPITATION_FIELD_NUMBER: _ClassVar[int]
    TRANSPARENT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    x_position: float
    y_position: float
    z_position: float
    echo_width: float
    device_id: int
    layer: int
    echo: int
    time_offset: int
    ground: bool
    dirt: bool
    precipitation: bool
    transparent: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., x_position: _Optional[float] = ..., y_position: _Optional[float] = ..., z_position: _Optional[float] = ..., echo_width: _Optional[float] = ..., device_id: _Optional[int] = ..., layer: _Optional[int] = ..., echo: _Optional[int] = ..., time_offset: _Optional[int] = ..., ground: bool = ..., dirt: bool = ..., precipitation: bool = ..., transparent: bool = ...) -> None: ...
