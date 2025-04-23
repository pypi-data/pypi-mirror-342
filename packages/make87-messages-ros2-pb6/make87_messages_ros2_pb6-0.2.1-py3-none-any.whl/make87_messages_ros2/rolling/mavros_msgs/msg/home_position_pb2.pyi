from make87_messages_ros2.rolling.geographic_msgs.msg import geo_point_pb2 as _geo_point_pb2
from make87_messages_ros2.rolling.geometry_msgs.msg import point_pb2 as _point_pb2
from make87_messages_ros2.rolling.geometry_msgs.msg import quaternion_pb2 as _quaternion_pb2
from make87_messages_ros2.rolling.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HomePosition(_message.Message):
    __slots__ = ("header", "geo", "position", "orientation", "approach")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    GEO_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    APPROACH_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    geo: _geo_point_pb2.GeoPoint
    position: _point_pb2.Point
    orientation: _quaternion_pb2.Quaternion
    approach: _vector3_pb2.Vector3
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., geo: _Optional[_Union[_geo_point_pb2.GeoPoint, _Mapping]] = ..., position: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., orientation: _Optional[_Union[_quaternion_pb2.Quaternion, _Mapping]] = ..., approach: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ...) -> None: ...
