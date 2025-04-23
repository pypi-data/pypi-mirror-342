from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class JointLimits(_message.Message):
    __slots__ = ("header", "joint_name", "has_position_limits", "min_position", "max_position", "has_velocity_limits", "max_velocity", "has_acceleration_limits", "max_acceleration", "has_jerk_limits", "max_jerk")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    JOINT_NAME_FIELD_NUMBER: _ClassVar[int]
    HAS_POSITION_LIMITS_FIELD_NUMBER: _ClassVar[int]
    MIN_POSITION_FIELD_NUMBER: _ClassVar[int]
    MAX_POSITION_FIELD_NUMBER: _ClassVar[int]
    HAS_VELOCITY_LIMITS_FIELD_NUMBER: _ClassVar[int]
    MAX_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    HAS_ACCELERATION_LIMITS_FIELD_NUMBER: _ClassVar[int]
    MAX_ACCELERATION_FIELD_NUMBER: _ClassVar[int]
    HAS_JERK_LIMITS_FIELD_NUMBER: _ClassVar[int]
    MAX_JERK_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    joint_name: str
    has_position_limits: bool
    min_position: float
    max_position: float
    has_velocity_limits: bool
    max_velocity: float
    has_acceleration_limits: bool
    max_acceleration: float
    has_jerk_limits: bool
    max_jerk: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., joint_name: _Optional[str] = ..., has_position_limits: bool = ..., min_position: _Optional[float] = ..., max_position: _Optional[float] = ..., has_velocity_limits: bool = ..., max_velocity: _Optional[float] = ..., has_acceleration_limits: bool = ..., max_acceleration: _Optional[float] = ..., has_jerk_limits: bool = ..., max_jerk: _Optional[float] = ...) -> None: ...
