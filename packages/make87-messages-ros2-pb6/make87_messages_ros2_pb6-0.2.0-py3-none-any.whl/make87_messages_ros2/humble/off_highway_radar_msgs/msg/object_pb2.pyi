from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.off_highway_radar_msgs.msg import object_a_pb2 as _object_a_pb2
from make87_messages_ros2.humble.off_highway_radar_msgs.msg import object_b_pb2 as _object_b_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Object(_message.Message):
    __slots__ = ("header", "ros2_header", "a", "b")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    A_FIELD_NUMBER: _ClassVar[int]
    B_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    a: _object_a_pb2.ObjectA
    b: _object_b_pb2.ObjectB
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., a: _Optional[_Union[_object_a_pb2.ObjectA, _Mapping]] = ..., b: _Optional[_Union[_object_b_pb2.ObjectB, _Mapping]] = ...) -> None: ...
