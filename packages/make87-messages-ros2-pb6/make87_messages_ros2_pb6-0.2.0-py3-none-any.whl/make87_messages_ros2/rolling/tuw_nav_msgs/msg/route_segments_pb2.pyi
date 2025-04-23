from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.rolling.tuw_nav_msgs.msg import route_segment_pb2 as _route_segment_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RouteSegments(_message.Message):
    __slots__ = ("header", "segments")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    segments: _containers.RepeatedCompositeFieldContainer[_route_segment_pb2.RouteSegment]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., segments: _Optional[_Iterable[_Union[_route_segment_pb2.RouteSegment, _Mapping]]] = ...) -> None: ...
