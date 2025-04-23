from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.off_highway_general_purpose_radar_msgs.msg import target_pb2 as _target_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Targets(_message.Message):
    __slots__ = ("header", "ros2_header", "targets")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    TARGETS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    targets: _containers.RepeatedCompositeFieldContainer[_target_pb2.Target]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., targets: _Optional[_Iterable[_Union[_target_pb2.Target, _Mapping]]] = ...) -> None: ...
