from make87_messages_ros2.rolling.marti_nav_msgs.msg import route_pb2 as _route_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetRouteListRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetRouteListResponse(_message.Message):
    __slots__ = ("routes", "success", "message")
    ROUTES_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    routes: _containers.RepeatedCompositeFieldContainer[_route_pb2.Route]
    success: bool
    message: str
    def __init__(self, routes: _Optional[_Iterable[_Union[_route_pb2.Route, _Mapping]]] = ..., success: bool = ..., message: _Optional[str] = ...) -> None: ...
