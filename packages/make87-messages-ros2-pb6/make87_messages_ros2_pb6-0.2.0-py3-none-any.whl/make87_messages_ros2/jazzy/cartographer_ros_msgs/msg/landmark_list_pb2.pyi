from make87_messages_ros2.jazzy.cartographer_ros_msgs.msg import landmark_entry_pb2 as _landmark_entry_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LandmarkList(_message.Message):
    __slots__ = ("header", "landmarks")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LANDMARKS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    landmarks: _containers.RepeatedCompositeFieldContainer[_landmark_entry_pb2.LandmarkEntry]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., landmarks: _Optional[_Iterable[_Union[_landmark_entry_pb2.LandmarkEntry, _Mapping]]] = ...) -> None: ...
