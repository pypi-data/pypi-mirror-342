from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NAVOdomVelocity(_message.Message):
    __slots__ = ("header", "vel_x", "vel_y", "omega", "timestamp", "coordbase")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VEL_X_FIELD_NUMBER: _ClassVar[int]
    VEL_Y_FIELD_NUMBER: _ClassVar[int]
    OMEGA_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    COORDBASE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    vel_x: float
    vel_y: float
    omega: float
    timestamp: int
    coordbase: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., vel_x: _Optional[float] = ..., vel_y: _Optional[float] = ..., omega: _Optional[float] = ..., timestamp: _Optional[int] = ..., coordbase: _Optional[int] = ...) -> None: ...
