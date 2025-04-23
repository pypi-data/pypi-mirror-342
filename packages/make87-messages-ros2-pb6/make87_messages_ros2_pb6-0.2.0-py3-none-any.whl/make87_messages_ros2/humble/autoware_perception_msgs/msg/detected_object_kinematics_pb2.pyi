from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_with_covariance_pb2 as _pose_with_covariance_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import twist_with_covariance_pb2 as _twist_with_covariance_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DetectedObjectKinematics(_message.Message):
    __slots__ = ("header", "pose_with_covariance", "has_position_covariance", "orientation_availability", "twist_with_covariance", "has_twist", "has_twist_covariance")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    POSE_WITH_COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    HAS_POSITION_COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
    TWIST_WITH_COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    HAS_TWIST_FIELD_NUMBER: _ClassVar[int]
    HAS_TWIST_COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    pose_with_covariance: _pose_with_covariance_pb2.PoseWithCovariance
    has_position_covariance: bool
    orientation_availability: int
    twist_with_covariance: _twist_with_covariance_pb2.TwistWithCovariance
    has_twist: bool
    has_twist_covariance: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., pose_with_covariance: _Optional[_Union[_pose_with_covariance_pb2.PoseWithCovariance, _Mapping]] = ..., has_position_covariance: bool = ..., orientation_availability: _Optional[int] = ..., twist_with_covariance: _Optional[_Union[_twist_with_covariance_pb2.TwistWithCovariance, _Mapping]] = ..., has_twist: bool = ..., has_twist_covariance: bool = ...) -> None: ...
