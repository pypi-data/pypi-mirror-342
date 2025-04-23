from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Base2DKinematics(_message.Message):
    __slots__ = ("header", "min_vel_x", "max_vel_x", "min_vel_y", "max_vel_y", "max_vel_theta", "acc_lim_x", "decel_lim_x", "acc_lim_y", "decel_lim_y", "acc_lim_theta", "decel_lim_theta", "min_speed_xy", "max_speed_xy", "min_speed_theta")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MIN_VEL_X_FIELD_NUMBER: _ClassVar[int]
    MAX_VEL_X_FIELD_NUMBER: _ClassVar[int]
    MIN_VEL_Y_FIELD_NUMBER: _ClassVar[int]
    MAX_VEL_Y_FIELD_NUMBER: _ClassVar[int]
    MAX_VEL_THETA_FIELD_NUMBER: _ClassVar[int]
    ACC_LIM_X_FIELD_NUMBER: _ClassVar[int]
    DECEL_LIM_X_FIELD_NUMBER: _ClassVar[int]
    ACC_LIM_Y_FIELD_NUMBER: _ClassVar[int]
    DECEL_LIM_Y_FIELD_NUMBER: _ClassVar[int]
    ACC_LIM_THETA_FIELD_NUMBER: _ClassVar[int]
    DECEL_LIM_THETA_FIELD_NUMBER: _ClassVar[int]
    MIN_SPEED_XY_FIELD_NUMBER: _ClassVar[int]
    MAX_SPEED_XY_FIELD_NUMBER: _ClassVar[int]
    MIN_SPEED_THETA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    min_vel_x: float
    max_vel_x: float
    min_vel_y: float
    max_vel_y: float
    max_vel_theta: float
    acc_lim_x: float
    decel_lim_x: float
    acc_lim_y: float
    decel_lim_y: float
    acc_lim_theta: float
    decel_lim_theta: float
    min_speed_xy: float
    max_speed_xy: float
    min_speed_theta: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., min_vel_x: _Optional[float] = ..., max_vel_x: _Optional[float] = ..., min_vel_y: _Optional[float] = ..., max_vel_y: _Optional[float] = ..., max_vel_theta: _Optional[float] = ..., acc_lim_x: _Optional[float] = ..., decel_lim_x: _Optional[float] = ..., acc_lim_y: _Optional[float] = ..., decel_lim_y: _Optional[float] = ..., acc_lim_theta: _Optional[float] = ..., decel_lim_theta: _Optional[float] = ..., min_speed_xy: _Optional[float] = ..., max_speed_xy: _Optional[float] = ..., min_speed_theta: _Optional[float] = ...) -> None: ...
