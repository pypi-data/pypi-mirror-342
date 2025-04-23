from make87_messages_ros2.rolling.geographic_msgs.msg import geo_point_pb2 as _geo_point_pb2
from make87_messages_ros2.rolling.geographic_msgs.msg import key_value_pb2 as _key_value_pb2
from make87_messages_ros2.rolling.unique_identifier_msgs.msg import uuid_pb2 as _uuid_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WayPoint(_message.Message):
    __slots__ = ("id", "position", "props")
    ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    PROPS_FIELD_NUMBER: _ClassVar[int]
    id: _uuid_pb2.UUID
    position: _geo_point_pb2.GeoPoint
    props: _containers.RepeatedCompositeFieldContainer[_key_value_pb2.KeyValue]
    def __init__(self, id: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., position: _Optional[_Union[_geo_point_pb2.GeoPoint, _Mapping]] = ..., props: _Optional[_Iterable[_Union[_key_value_pb2.KeyValue, _Mapping]]] = ...) -> None: ...
