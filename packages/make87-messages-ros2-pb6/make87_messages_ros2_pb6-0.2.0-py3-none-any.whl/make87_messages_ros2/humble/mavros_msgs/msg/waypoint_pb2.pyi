from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Waypoint(_message.Message):
    __slots__ = ("header", "frame", "command", "is_current", "autocontinue", "param1", "param2", "param3", "param4", "x_lat", "y_long", "z_alt")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FRAME_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    IS_CURRENT_FIELD_NUMBER: _ClassVar[int]
    AUTOCONTINUE_FIELD_NUMBER: _ClassVar[int]
    PARAM1_FIELD_NUMBER: _ClassVar[int]
    PARAM2_FIELD_NUMBER: _ClassVar[int]
    PARAM3_FIELD_NUMBER: _ClassVar[int]
    PARAM4_FIELD_NUMBER: _ClassVar[int]
    X_LAT_FIELD_NUMBER: _ClassVar[int]
    Y_LONG_FIELD_NUMBER: _ClassVar[int]
    Z_ALT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    frame: int
    command: int
    is_current: bool
    autocontinue: bool
    param1: float
    param2: float
    param3: float
    param4: float
    x_lat: float
    y_long: float
    z_alt: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., frame: _Optional[int] = ..., command: _Optional[int] = ..., is_current: bool = ..., autocontinue: bool = ..., param1: _Optional[float] = ..., param2: _Optional[float] = ..., param3: _Optional[float] = ..., param4: _Optional[float] = ..., x_lat: _Optional[float] = ..., y_long: _Optional[float] = ..., z_alt: _Optional[float] = ...) -> None: ...
