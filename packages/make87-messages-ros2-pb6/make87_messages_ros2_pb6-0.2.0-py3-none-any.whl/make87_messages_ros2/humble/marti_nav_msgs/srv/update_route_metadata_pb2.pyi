from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.marti_nav_msgs.msg import route_point_pb2 as _route_point_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UpdateRouteMetadataRequest(_message.Message):
    __slots__ = ("header", "route_guid", "metadata_points")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROUTE_GUID_FIELD_NUMBER: _ClassVar[int]
    METADATA_POINTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    route_guid: str
    metadata_points: _containers.RepeatedCompositeFieldContainer[_route_point_pb2.RoutePoint]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., route_guid: _Optional[str] = ..., metadata_points: _Optional[_Iterable[_Union[_route_point_pb2.RoutePoint, _Mapping]]] = ...) -> None: ...

class UpdateRouteMetadataResponse(_message.Message):
    __slots__ = ("header", "success", "message")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    message: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., message: _Optional[str] = ...) -> None: ...
