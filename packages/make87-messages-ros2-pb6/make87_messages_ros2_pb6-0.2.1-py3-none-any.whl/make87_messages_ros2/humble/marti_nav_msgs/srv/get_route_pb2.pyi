from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.marti_nav_msgs.msg import route_pb2 as _route_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetRouteRequest(_message.Message):
    __slots__ = ("header", "guid")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    GUID_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    guid: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., guid: _Optional[str] = ...) -> None: ...

class GetRouteResponse(_message.Message):
    __slots__ = ("header", "route", "success", "message")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROUTE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    route: _route_pb2.Route
    success: bool
    message: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., route: _Optional[_Union[_route_pb2.Route, _Mapping]] = ..., success: bool = ..., message: _Optional[str] = ...) -> None: ...
