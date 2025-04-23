from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AckermannDrive(_message.Message):
    __slots__ = ("header", "steering_angle", "steering_angle_velocity", "speed", "acceleration", "jerk")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STEERING_ANGLE_FIELD_NUMBER: _ClassVar[int]
    STEERING_ANGLE_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    ACCELERATION_FIELD_NUMBER: _ClassVar[int]
    JERK_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    steering_angle: float
    steering_angle_velocity: float
    speed: float
    acceleration: float
    jerk: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., steering_angle: _Optional[float] = ..., steering_angle_velocity: _Optional[float] = ..., speed: _Optional[float] = ..., acceleration: _Optional[float] = ..., jerk: _Optional[float] = ...) -> None: ...
