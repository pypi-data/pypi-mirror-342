from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geographic_msgs.msg import geo_point_pb2 as _geo_point_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import quaternion_pb2 as _quaternion_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GeoPose(_message.Message):
    __slots__ = ("header", "position", "orientation")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    position: _geo_point_pb2.GeoPoint
    orientation: _quaternion_pb2.Quaternion
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., position: _Optional[_Union[_geo_point_pb2.GeoPoint, _Mapping]] = ..., orientation: _Optional[_Union[_quaternion_pb2.Quaternion, _Mapping]] = ...) -> None: ...
