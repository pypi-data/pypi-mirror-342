from make87_messages_ros2.jazzy.builtin_interfaces.msg import duration_pb2 as _duration_pb2
from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_pb2 as _pose_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TrajectoryPoint(_message.Message):
    __slots__ = ("time_from_start", "pose", "longitudinal_velocity_mps", "lateral_velocity_mps", "acceleration_mps2", "heading_rate_rps", "front_wheel_angle_rad", "rear_wheel_angle_rad")
    TIME_FROM_START_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDINAL_VELOCITY_MPS_FIELD_NUMBER: _ClassVar[int]
    LATERAL_VELOCITY_MPS_FIELD_NUMBER: _ClassVar[int]
    ACCELERATION_MPS2_FIELD_NUMBER: _ClassVar[int]
    HEADING_RATE_RPS_FIELD_NUMBER: _ClassVar[int]
    FRONT_WHEEL_ANGLE_RAD_FIELD_NUMBER: _ClassVar[int]
    REAR_WHEEL_ANGLE_RAD_FIELD_NUMBER: _ClassVar[int]
    time_from_start: _duration_pb2.Duration
    pose: _pose_pb2.Pose
    longitudinal_velocity_mps: float
    lateral_velocity_mps: float
    acceleration_mps2: float
    heading_rate_rps: float
    front_wheel_angle_rad: float
    rear_wheel_angle_rad: float
    def __init__(self, time_from_start: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., longitudinal_velocity_mps: _Optional[float] = ..., lateral_velocity_mps: _Optional[float] = ..., acceleration_mps2: _Optional[float] = ..., heading_rate_rps: _Optional[float] = ..., front_wheel_angle_rad: _Optional[float] = ..., rear_wheel_angle_rad: _Optional[float] = ...) -> None: ...
