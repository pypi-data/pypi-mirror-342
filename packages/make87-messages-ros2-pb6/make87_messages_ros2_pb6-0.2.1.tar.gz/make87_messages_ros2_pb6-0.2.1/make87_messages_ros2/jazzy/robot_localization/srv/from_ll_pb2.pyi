from make87_messages_ros2.jazzy.geographic_msgs.msg import geo_point_pb2 as _geo_point_pb2
from make87_messages_ros2.jazzy.geometry_msgs.msg import point_pb2 as _point_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FromLLRequest(_message.Message):
    __slots__ = ("ll_point",)
    LL_POINT_FIELD_NUMBER: _ClassVar[int]
    ll_point: _geo_point_pb2.GeoPoint
    def __init__(self, ll_point: _Optional[_Union[_geo_point_pb2.GeoPoint, _Mapping]] = ...) -> None: ...

class FromLLResponse(_message.Message):
    __slots__ = ("map_point",)
    MAP_POINT_FIELD_NUMBER: _ClassVar[int]
    map_point: _point_pb2.Point
    def __init__(self, map_point: _Optional[_Union[_point_pb2.Point, _Mapping]] = ...) -> None: ...
