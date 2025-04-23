from make87_messages_ros2.jazzy.geographic_msgs.msg import bounding_box_pb2 as _bounding_box_pb2
from make87_messages_ros2.jazzy.geographic_msgs.msg import key_value_pb2 as _key_value_pb2
from make87_messages_ros2.jazzy.geographic_msgs.msg import map_feature_pb2 as _map_feature_pb2
from make87_messages_ros2.jazzy.geographic_msgs.msg import way_point_pb2 as _way_point_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.jazzy.unique_identifier_msgs.msg import uuid_pb2 as _uuid_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GeographicMap(_message.Message):
    __slots__ = ("header", "id", "bounds", "points", "features", "props")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    BOUNDS_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    PROPS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    id: _uuid_pb2.UUID
    bounds: _bounding_box_pb2.BoundingBox
    points: _containers.RepeatedCompositeFieldContainer[_way_point_pb2.WayPoint]
    features: _containers.RepeatedCompositeFieldContainer[_map_feature_pb2.MapFeature]
    props: _containers.RepeatedCompositeFieldContainer[_key_value_pb2.KeyValue]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., id: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., bounds: _Optional[_Union[_bounding_box_pb2.BoundingBox, _Mapping]] = ..., points: _Optional[_Iterable[_Union[_way_point_pb2.WayPoint, _Mapping]]] = ..., features: _Optional[_Iterable[_Union[_map_feature_pb2.MapFeature, _Mapping]]] = ..., props: _Optional[_Iterable[_Union[_key_value_pb2.KeyValue, _Mapping]]] = ...) -> None: ...
