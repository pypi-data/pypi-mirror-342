from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import point_cloud2_pb2 as _point_cloud2_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetPointmapLayerRequest(_message.Message):
    __slots__ = ("header", "layer_name")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LAYER_NAME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    layer_name: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., layer_name: _Optional[str] = ...) -> None: ...

class GetPointmapLayerResponse(_message.Message):
    __slots__ = ("header", "valid", "points")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VALID_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    valid: bool
    points: _point_cloud2_pb2.PointCloud2
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., valid: bool = ..., points: _Optional[_Union[_point_cloud2_pb2.PointCloud2, _Mapping]] = ...) -> None: ...
