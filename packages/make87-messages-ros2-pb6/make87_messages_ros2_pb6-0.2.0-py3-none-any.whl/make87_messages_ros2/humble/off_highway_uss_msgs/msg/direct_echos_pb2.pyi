from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.off_highway_uss_msgs.msg import direct_echo_pb2 as _direct_echo_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DirectEchos(_message.Message):
    __slots__ = ("header", "ros2_header", "direct_echos")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    DIRECT_ECHOS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    direct_echos: _containers.RepeatedCompositeFieldContainer[_direct_echo_pb2.DirectEcho]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., direct_echos: _Optional[_Iterable[_Union[_direct_echo_pb2.DirectEcho, _Mapping]]] = ...) -> None: ...
