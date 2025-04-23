from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NavigationFeedback(_message.Message):
    __slots__ = ("header", "total_waypoints", "reached_waypoints")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TOTAL_WAYPOINTS_FIELD_NUMBER: _ClassVar[int]
    REACHED_WAYPOINTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    total_waypoints: int
    reached_waypoints: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., total_waypoints: _Optional[int] = ..., reached_waypoints: _Optional[int] = ...) -> None: ...
