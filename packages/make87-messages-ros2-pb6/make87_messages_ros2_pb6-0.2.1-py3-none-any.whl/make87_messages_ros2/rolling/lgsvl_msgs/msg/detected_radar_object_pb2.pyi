from make87_messages_ros2.rolling.geometry_msgs.msg import point_pb2 as _point_pb2
from make87_messages_ros2.rolling.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DetectedRadarObject(_message.Message):
    __slots__ = ("id", "sensor_aim", "sensor_right", "sensor_position", "sensor_velocity", "sensor_angle", "object_position", "object_velocity", "object_relative_position", "object_relative_velocity", "object_collider_size", "object_state", "new_detection")
    ID_FIELD_NUMBER: _ClassVar[int]
    SENSOR_AIM_FIELD_NUMBER: _ClassVar[int]
    SENSOR_RIGHT_FIELD_NUMBER: _ClassVar[int]
    SENSOR_POSITION_FIELD_NUMBER: _ClassVar[int]
    SENSOR_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    SENSOR_ANGLE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_POSITION_FIELD_NUMBER: _ClassVar[int]
    OBJECT_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    OBJECT_RELATIVE_POSITION_FIELD_NUMBER: _ClassVar[int]
    OBJECT_RELATIVE_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    OBJECT_COLLIDER_SIZE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_STATE_FIELD_NUMBER: _ClassVar[int]
    NEW_DETECTION_FIELD_NUMBER: _ClassVar[int]
    id: int
    sensor_aim: _vector3_pb2.Vector3
    sensor_right: _vector3_pb2.Vector3
    sensor_position: _point_pb2.Point
    sensor_velocity: _vector3_pb2.Vector3
    sensor_angle: float
    object_position: _point_pb2.Point
    object_velocity: _vector3_pb2.Vector3
    object_relative_position: _point_pb2.Point
    object_relative_velocity: _vector3_pb2.Vector3
    object_collider_size: _vector3_pb2.Vector3
    object_state: int
    new_detection: bool
    def __init__(self, id: _Optional[int] = ..., sensor_aim: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., sensor_right: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., sensor_position: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., sensor_velocity: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., sensor_angle: _Optional[float] = ..., object_position: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., object_velocity: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., object_relative_position: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., object_relative_velocity: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., object_collider_size: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., object_state: _Optional[int] = ..., new_detection: bool = ...) -> None: ...
