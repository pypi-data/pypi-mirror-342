from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WorkspaceParameters(_message.Message):
    __slots__ = ("header", "ros2_header", "min_corner", "max_corner")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    MIN_CORNER_FIELD_NUMBER: _ClassVar[int]
    MAX_CORNER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    min_corner: _vector3_pb2.Vector3
    max_corner: _vector3_pb2.Vector3
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., min_corner: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., max_corner: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ...) -> None: ...
