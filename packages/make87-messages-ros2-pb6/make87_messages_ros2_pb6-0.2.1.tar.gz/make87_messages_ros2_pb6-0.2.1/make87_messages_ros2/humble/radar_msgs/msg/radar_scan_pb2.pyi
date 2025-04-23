from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.radar_msgs.msg import radar_return_pb2 as _radar_return_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RadarScan(_message.Message):
    __slots__ = ("header", "ros2_header", "returns")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    RETURNS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    returns: _containers.RepeatedCompositeFieldContainer[_radar_return_pb2.RadarReturn]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., returns: _Optional[_Iterable[_Union[_radar_return_pb2.RadarReturn, _Mapping]]] = ...) -> None: ...
