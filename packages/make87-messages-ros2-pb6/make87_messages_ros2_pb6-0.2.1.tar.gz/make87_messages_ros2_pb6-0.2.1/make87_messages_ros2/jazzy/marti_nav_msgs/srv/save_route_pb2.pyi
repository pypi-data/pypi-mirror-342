from make87_messages_ros2.jazzy.marti_nav_msgs.msg import route_pb2 as _route_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SaveRouteRequest(_message.Message):
    __slots__ = ("name", "guid", "route", "thumbnail")
    NAME_FIELD_NUMBER: _ClassVar[int]
    GUID_FIELD_NUMBER: _ClassVar[int]
    ROUTE_FIELD_NUMBER: _ClassVar[int]
    THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    name: str
    guid: str
    route: _route_pb2.Route
    thumbnail: str
    def __init__(self, name: _Optional[str] = ..., guid: _Optional[str] = ..., route: _Optional[_Union[_route_pb2.Route, _Mapping]] = ..., thumbnail: _Optional[str] = ...) -> None: ...

class SaveRouteResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...
