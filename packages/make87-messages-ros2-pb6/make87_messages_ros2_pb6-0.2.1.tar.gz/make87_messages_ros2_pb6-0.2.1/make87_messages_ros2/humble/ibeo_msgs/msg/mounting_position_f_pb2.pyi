from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MountingPositionF(_message.Message):
    __slots__ = ("header", "yaw_angle", "pitch_angle", "roll_angle", "x_position", "y_position", "z_position")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    YAW_ANGLE_FIELD_NUMBER: _ClassVar[int]
    PITCH_ANGLE_FIELD_NUMBER: _ClassVar[int]
    ROLL_ANGLE_FIELD_NUMBER: _ClassVar[int]
    X_POSITION_FIELD_NUMBER: _ClassVar[int]
    Y_POSITION_FIELD_NUMBER: _ClassVar[int]
    Z_POSITION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    yaw_angle: float
    pitch_angle: float
    roll_angle: float
    x_position: float
    y_position: float
    z_position: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., yaw_angle: _Optional[float] = ..., pitch_angle: _Optional[float] = ..., roll_angle: _Optional[float] = ..., x_position: _Optional[float] = ..., y_position: _Optional[float] = ..., z_position: _Optional[float] = ...) -> None: ...
