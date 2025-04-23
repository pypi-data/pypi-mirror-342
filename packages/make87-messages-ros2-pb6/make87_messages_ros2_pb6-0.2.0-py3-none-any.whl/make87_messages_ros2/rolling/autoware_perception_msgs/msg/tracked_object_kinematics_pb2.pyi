from make87_messages_ros2.rolling.geometry_msgs.msg import accel_with_covariance_pb2 as _accel_with_covariance_pb2
from make87_messages_ros2.rolling.geometry_msgs.msg import pose_with_covariance_pb2 as _pose_with_covariance_pb2
from make87_messages_ros2.rolling.geometry_msgs.msg import twist_with_covariance_pb2 as _twist_with_covariance_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TrackedObjectKinematics(_message.Message):
    __slots__ = ("pose_with_covariance", "twist_with_covariance", "acceleration_with_covariance", "orientation_availability", "is_stationary")
    POSE_WITH_COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    TWIST_WITH_COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    ACCELERATION_WITH_COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
    IS_STATIONARY_FIELD_NUMBER: _ClassVar[int]
    pose_with_covariance: _pose_with_covariance_pb2.PoseWithCovariance
    twist_with_covariance: _twist_with_covariance_pb2.TwistWithCovariance
    acceleration_with_covariance: _accel_with_covariance_pb2.AccelWithCovariance
    orientation_availability: int
    is_stationary: bool
    def __init__(self, pose_with_covariance: _Optional[_Union[_pose_with_covariance_pb2.PoseWithCovariance, _Mapping]] = ..., twist_with_covariance: _Optional[_Union[_twist_with_covariance_pb2.TwistWithCovariance, _Mapping]] = ..., acceleration_with_covariance: _Optional[_Union[_accel_with_covariance_pb2.AccelWithCovariance, _Mapping]] = ..., orientation_availability: _Optional[int] = ..., is_stationary: bool = ...) -> None: ...
