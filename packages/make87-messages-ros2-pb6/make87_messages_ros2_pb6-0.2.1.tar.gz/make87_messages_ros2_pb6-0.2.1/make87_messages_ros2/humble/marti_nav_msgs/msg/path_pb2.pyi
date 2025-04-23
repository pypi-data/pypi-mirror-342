from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.marti_nav_msgs.msg import path_point_pb2 as _path_point_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Path(_message.Message):
    __slots__ = ("header", "ros2_header", "points", "in_reverse")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    IN_REVERSE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    points: _containers.RepeatedCompositeFieldContainer[_path_point_pb2.PathPoint]
    in_reverse: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., points: _Optional[_Iterable[_Union[_path_point_pb2.PathPoint, _Mapping]]] = ..., in_reverse: bool = ...) -> None: ...
