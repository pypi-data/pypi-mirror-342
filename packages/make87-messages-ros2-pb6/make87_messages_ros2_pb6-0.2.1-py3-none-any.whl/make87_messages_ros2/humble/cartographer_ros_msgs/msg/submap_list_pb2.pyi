from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.cartographer_ros_msgs.msg import submap_entry_pb2 as _submap_entry_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SubmapList(_message.Message):
    __slots__ = ("header", "ros2_header", "submap")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    SUBMAP_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    submap: _containers.RepeatedCompositeFieldContainer[_submap_entry_pb2.SubmapEntry]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., submap: _Optional[_Iterable[_Union[_submap_entry_pb2.SubmapEntry, _Mapping]]] = ...) -> None: ...
