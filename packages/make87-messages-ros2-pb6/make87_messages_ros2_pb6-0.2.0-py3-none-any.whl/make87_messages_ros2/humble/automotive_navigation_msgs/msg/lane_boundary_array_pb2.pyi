from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.automotive_navigation_msgs.msg import lane_boundary_pb2 as _lane_boundary_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LaneBoundaryArray(_message.Message):
    __slots__ = ("header", "boundaries")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BOUNDARIES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    boundaries: _containers.RepeatedCompositeFieldContainer[_lane_boundary_pb2.LaneBoundary]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., boundaries: _Optional[_Iterable[_Union[_lane_boundary_pb2.LaneBoundary, _Mapping]]] = ...) -> None: ...
