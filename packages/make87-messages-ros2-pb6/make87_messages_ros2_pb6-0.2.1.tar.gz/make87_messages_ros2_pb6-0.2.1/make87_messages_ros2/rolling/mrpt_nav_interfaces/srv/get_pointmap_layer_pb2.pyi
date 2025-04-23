from make87_messages_ros2.rolling.sensor_msgs.msg import point_cloud2_pb2 as _point_cloud2_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetPointmapLayerRequest(_message.Message):
    __slots__ = ("layer_name",)
    LAYER_NAME_FIELD_NUMBER: _ClassVar[int]
    layer_name: str
    def __init__(self, layer_name: _Optional[str] = ...) -> None: ...

class GetPointmapLayerResponse(_message.Message):
    __slots__ = ("valid", "points")
    VALID_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    valid: bool
    points: _point_cloud2_pb2.PointCloud2
    def __init__(self, valid: bool = ..., points: _Optional[_Union[_point_cloud2_pb2.PointCloud2, _Mapping]] = ...) -> None: ...
