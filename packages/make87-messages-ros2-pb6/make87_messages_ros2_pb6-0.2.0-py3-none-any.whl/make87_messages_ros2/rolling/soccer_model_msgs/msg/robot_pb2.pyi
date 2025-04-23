from make87_messages_ros2.rolling.geometry_msgs.msg import pose_with_covariance_pb2 as _pose_with_covariance_pb2
from make87_messages_ros2.rolling.geometry_msgs.msg import twist_with_covariance_pb2 as _twist_with_covariance_pb2
from make87_messages_ros2.rolling.soccer_vision_attribute_msgs.msg import robot_pb2 as _robot_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Robot(_message.Message):
    __slots__ = ("pose", "twist", "attributes")
    POSE_FIELD_NUMBER: _ClassVar[int]
    TWIST_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    pose: _pose_with_covariance_pb2.PoseWithCovariance
    twist: _twist_with_covariance_pb2.TwistWithCovariance
    attributes: _robot_pb2.Robot
    def __init__(self, pose: _Optional[_Union[_pose_with_covariance_pb2.PoseWithCovariance, _Mapping]] = ..., twist: _Optional[_Union[_twist_with_covariance_pb2.TwistWithCovariance, _Mapping]] = ..., attributes: _Optional[_Union[_robot_pb2.Robot, _Mapping]] = ...) -> None: ...
