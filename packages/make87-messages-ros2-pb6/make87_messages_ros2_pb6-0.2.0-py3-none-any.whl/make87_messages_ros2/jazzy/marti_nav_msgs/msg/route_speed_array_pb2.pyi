from make87_messages_ros2.jazzy.marti_nav_msgs.msg import route_speed_pb2 as _route_speed_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RouteSpeedArray(_message.Message):
    __slots__ = ("header", "speeds")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SPEEDS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    speeds: _containers.RepeatedCompositeFieldContainer[_route_speed_pb2.RouteSpeed]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., speeds: _Optional[_Iterable[_Union[_route_speed_pb2.RouteSpeed, _Mapping]]] = ...) -> None: ...
