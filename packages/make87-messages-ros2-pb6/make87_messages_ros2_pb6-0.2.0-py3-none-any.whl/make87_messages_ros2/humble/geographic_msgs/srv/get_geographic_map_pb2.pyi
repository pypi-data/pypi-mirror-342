from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geographic_msgs.msg import bounding_box_pb2 as _bounding_box_pb2
from make87_messages_ros2.humble.geographic_msgs.msg import geographic_map_pb2 as _geographic_map_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetGeographicMapRequest(_message.Message):
    __slots__ = ("header", "url", "bounds")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    BOUNDS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    url: str
    bounds: _bounding_box_pb2.BoundingBox
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., url: _Optional[str] = ..., bounds: _Optional[_Union[_bounding_box_pb2.BoundingBox, _Mapping]] = ...) -> None: ...

class GetGeographicMapResponse(_message.Message):
    __slots__ = ("header", "success", "status", "map")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MAP_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    status: str
    map: _geographic_map_pb2.GeographicMap
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., status: _Optional[str] = ..., map: _Optional[_Union[_geographic_map_pb2.GeographicMap, _Mapping]] = ...) -> None: ...
