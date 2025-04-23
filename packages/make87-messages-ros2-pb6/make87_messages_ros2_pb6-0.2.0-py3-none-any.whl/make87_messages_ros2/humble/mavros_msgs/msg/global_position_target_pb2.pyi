from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GlobalPositionTarget(_message.Message):
    __slots__ = ("header", "ros2_header", "coordinate_frame", "type_mask", "latitude", "longitude", "altitude", "velocity", "acceleration_or_force", "yaw", "yaw_rate")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    COORDINATE_FRAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_MASK_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_FIELD_NUMBER: _ClassVar[int]
    ACCELERATION_OR_FORCE_FIELD_NUMBER: _ClassVar[int]
    YAW_FIELD_NUMBER: _ClassVar[int]
    YAW_RATE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    coordinate_frame: int
    type_mask: int
    latitude: float
    longitude: float
    altitude: float
    velocity: _vector3_pb2.Vector3
    acceleration_or_force: _vector3_pb2.Vector3
    yaw: float
    yaw_rate: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., coordinate_frame: _Optional[int] = ..., type_mask: _Optional[int] = ..., latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., altitude: _Optional[float] = ..., velocity: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., acceleration_or_force: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., yaw: _Optional[float] = ..., yaw_rate: _Optional[float] = ...) -> None: ...
