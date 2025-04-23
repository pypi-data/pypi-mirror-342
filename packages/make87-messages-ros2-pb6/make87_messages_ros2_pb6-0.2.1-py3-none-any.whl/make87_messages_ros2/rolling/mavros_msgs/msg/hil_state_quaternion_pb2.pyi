from make87_messages_ros2.rolling.geographic_msgs.msg import geo_point_pb2 as _geo_point_pb2
from make87_messages_ros2.rolling.geometry_msgs.msg import quaternion_pb2 as _quaternion_pb2
from make87_messages_ros2.rolling.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HilStateQuaternion(_message.Message):
    __slots__ = ("header", "orientation", "angular_velocity", "linear_acceleration", "linear_velocity", "geo", "ind_airspeed", "true_airspeed")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    LINEAR_ACCELERATION_FIELD_NUMBER: _ClassVar[int]
    LINEAR_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    GEO_FIELD_NUMBER: _ClassVar[int]
    IND_AIRSPEED_FIELD_NUMBER: _ClassVar[int]
    TRUE_AIRSPEED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    orientation: _quaternion_pb2.Quaternion
    angular_velocity: _vector3_pb2.Vector3
    linear_acceleration: _vector3_pb2.Vector3
    linear_velocity: _vector3_pb2.Vector3
    geo: _geo_point_pb2.GeoPoint
    ind_airspeed: float
    true_airspeed: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., orientation: _Optional[_Union[_quaternion_pb2.Quaternion, _Mapping]] = ..., angular_velocity: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., linear_acceleration: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., linear_velocity: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., geo: _Optional[_Union[_geo_point_pb2.GeoPoint, _Mapping]] = ..., ind_airspeed: _Optional[float] = ..., true_airspeed: _Optional[float] = ...) -> None: ...
