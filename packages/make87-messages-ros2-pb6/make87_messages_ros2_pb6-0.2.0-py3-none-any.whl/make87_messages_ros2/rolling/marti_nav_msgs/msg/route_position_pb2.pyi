from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RoutePosition(_message.Message):
    __slots__ = ("header", "route_id", "id", "distance")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROUTE_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    route_id: str
    id: str
    distance: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., route_id: _Optional[str] = ..., id: _Optional[str] = ..., distance: _Optional[float] = ...) -> None: ...
