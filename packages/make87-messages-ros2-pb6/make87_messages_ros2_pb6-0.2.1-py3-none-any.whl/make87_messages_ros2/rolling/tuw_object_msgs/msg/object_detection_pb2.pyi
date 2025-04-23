from make87_messages_ros2.rolling.geometry_msgs.msg import quaternion_pb2 as _quaternion_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.rolling.tuw_object_msgs.msg import object_with_covariance_pb2 as _object_with_covariance_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ObjectDetection(_message.Message):
    __slots__ = ("header", "distance_min", "distance_max", "distance_max_id", "view_direction", "fov_horizontal", "fov_vertical", "type", "objects", "sensor_type")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_MIN_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_MAX_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_MAX_ID_FIELD_NUMBER: _ClassVar[int]
    VIEW_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    FOV_HORIZONTAL_FIELD_NUMBER: _ClassVar[int]
    FOV_VERTICAL_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    OBJECTS_FIELD_NUMBER: _ClassVar[int]
    SENSOR_TYPE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    distance_min: float
    distance_max: float
    distance_max_id: float
    view_direction: _quaternion_pb2.Quaternion
    fov_horizontal: float
    fov_vertical: float
    type: str
    objects: _containers.RepeatedCompositeFieldContainer[_object_with_covariance_pb2.ObjectWithCovariance]
    sensor_type: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., distance_min: _Optional[float] = ..., distance_max: _Optional[float] = ..., distance_max_id: _Optional[float] = ..., view_direction: _Optional[_Union[_quaternion_pb2.Quaternion, _Mapping]] = ..., fov_horizontal: _Optional[float] = ..., fov_vertical: _Optional[float] = ..., type: _Optional[str] = ..., objects: _Optional[_Iterable[_Union[_object_with_covariance_pb2.ObjectWithCovariance, _Mapping]]] = ..., sensor_type: _Optional[str] = ...) -> None: ...
