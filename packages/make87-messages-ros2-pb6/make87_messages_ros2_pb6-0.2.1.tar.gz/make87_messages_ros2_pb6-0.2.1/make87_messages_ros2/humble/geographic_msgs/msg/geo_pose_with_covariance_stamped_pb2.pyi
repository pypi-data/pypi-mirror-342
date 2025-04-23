from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geographic_msgs.msg import geo_pose_with_covariance_pb2 as _geo_pose_with_covariance_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GeoPoseWithCovarianceStamped(_message.Message):
    __slots__ = ("header", "ros2_header", "pose")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    pose: _geo_pose_with_covariance_pb2.GeoPoseWithCovariance
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., pose: _Optional[_Union[_geo_pose_with_covariance_pb2.GeoPoseWithCovariance, _Mapping]] = ...) -> None: ...
