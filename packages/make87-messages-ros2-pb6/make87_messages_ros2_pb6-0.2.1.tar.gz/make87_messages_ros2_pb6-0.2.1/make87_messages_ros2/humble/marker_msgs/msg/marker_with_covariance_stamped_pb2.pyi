from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.marker_msgs.msg import marker_with_covariance_pb2 as _marker_with_covariance_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MarkerWithCovarianceStamped(_message.Message):
    __slots__ = ("header", "ros2_header", "marker")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    MARKER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    marker: _marker_with_covariance_pb2.MarkerWithCovariance
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., marker: _Optional[_Union[_marker_with_covariance_pb2.MarkerWithCovariance, _Mapping]] = ...) -> None: ...
