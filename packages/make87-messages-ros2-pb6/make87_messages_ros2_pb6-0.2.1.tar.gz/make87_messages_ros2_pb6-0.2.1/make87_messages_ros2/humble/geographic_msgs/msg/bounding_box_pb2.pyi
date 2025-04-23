from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geographic_msgs.msg import geo_point_pb2 as _geo_point_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BoundingBox(_message.Message):
    __slots__ = ("header", "min_pt", "max_pt")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MIN_PT_FIELD_NUMBER: _ClassVar[int]
    MAX_PT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    min_pt: _geo_point_pb2.GeoPoint
    max_pt: _geo_point_pb2.GeoPoint
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., min_pt: _Optional[_Union[_geo_point_pb2.GeoPoint, _Mapping]] = ..., max_pt: _Optional[_Union[_geo_point_pb2.GeoPoint, _Mapping]] = ...) -> None: ...
