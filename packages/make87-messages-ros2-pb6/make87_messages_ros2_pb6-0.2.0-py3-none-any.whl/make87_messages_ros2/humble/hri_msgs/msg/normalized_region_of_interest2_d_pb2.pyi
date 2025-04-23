from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NormalizedRegionOfInterest2D(_message.Message):
    __slots__ = ("header", "ros2_header", "xmin", "ymin", "xmax", "ymax", "c")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    XMIN_FIELD_NUMBER: _ClassVar[int]
    YMIN_FIELD_NUMBER: _ClassVar[int]
    XMAX_FIELD_NUMBER: _ClassVar[int]
    YMAX_FIELD_NUMBER: _ClassVar[int]
    C_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    xmin: float
    ymin: float
    xmax: float
    ymax: float
    c: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., xmin: _Optional[float] = ..., ymin: _Optional[float] = ..., xmax: _Optional[float] = ..., ymax: _Optional[float] = ..., c: _Optional[float] = ...) -> None: ...
