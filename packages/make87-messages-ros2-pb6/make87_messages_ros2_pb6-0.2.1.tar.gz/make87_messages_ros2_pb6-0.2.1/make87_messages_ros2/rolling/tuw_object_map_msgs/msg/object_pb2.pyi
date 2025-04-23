from make87_messages_ros2.rolling.geometry_msgs.msg import point_pb2 as _point_pb2
from make87_messages_ros2.rolling.tuw_object_map_msgs.msg import geo_point_pb2 as _geo_point_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Object(_message.Message):
    __slots__ = ("id", "type", "geo_points", "map_points", "enflation_radius", "bondary_radius")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    GEO_POINTS_FIELD_NUMBER: _ClassVar[int]
    MAP_POINTS_FIELD_NUMBER: _ClassVar[int]
    ENFLATION_RADIUS_FIELD_NUMBER: _ClassVar[int]
    BONDARY_RADIUS_FIELD_NUMBER: _ClassVar[int]
    id: int
    type: int
    geo_points: _containers.RepeatedCompositeFieldContainer[_geo_point_pb2.GeoPoint]
    map_points: _containers.RepeatedCompositeFieldContainer[_point_pb2.Point]
    enflation_radius: _containers.RepeatedScalarFieldContainer[float]
    bondary_radius: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, id: _Optional[int] = ..., type: _Optional[int] = ..., geo_points: _Optional[_Iterable[_Union[_geo_point_pb2.GeoPoint, _Mapping]]] = ..., map_points: _Optional[_Iterable[_Union[_point_pb2.Point, _Mapping]]] = ..., enflation_radius: _Optional[_Iterable[float]] = ..., bondary_radius: _Optional[_Iterable[float]] = ...) -> None: ...
