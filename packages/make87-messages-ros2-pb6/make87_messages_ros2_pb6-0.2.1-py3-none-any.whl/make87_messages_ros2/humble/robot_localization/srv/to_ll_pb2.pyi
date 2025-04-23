from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geographic_msgs.msg import geo_point_pb2 as _geo_point_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import point_pb2 as _point_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ToLLRequest(_message.Message):
    __slots__ = ("header", "map_point")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MAP_POINT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    map_point: _point_pb2.Point
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., map_point: _Optional[_Union[_point_pb2.Point, _Mapping]] = ...) -> None: ...

class ToLLResponse(_message.Message):
    __slots__ = ("header", "ll_point")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LL_POINT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ll_point: _geo_point_pb2.GeoPoint
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ll_point: _Optional[_Union[_geo_point_pb2.GeoPoint, _Mapping]] = ...) -> None: ...
