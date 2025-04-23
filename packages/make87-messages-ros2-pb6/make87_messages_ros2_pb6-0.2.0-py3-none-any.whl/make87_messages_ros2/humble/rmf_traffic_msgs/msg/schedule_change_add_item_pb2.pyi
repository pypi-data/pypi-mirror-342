from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import route_pb2 as _route_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScheduleChangeAddItem(_message.Message):
    __slots__ = ("header", "route_id", "storage_id", "route")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROUTE_ID_FIELD_NUMBER: _ClassVar[int]
    STORAGE_ID_FIELD_NUMBER: _ClassVar[int]
    ROUTE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    route_id: int
    storage_id: int
    route: _route_pb2.Route
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., route_id: _Optional[int] = ..., storage_id: _Optional[int] = ..., route: _Optional[_Union[_route_pb2.Route, _Mapping]] = ...) -> None: ...
