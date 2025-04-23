from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Dvl(_message.Message):
    __slots__ = ("header", "ros2_header", "velocity_mode", "dvl_type", "velocity", "velocity_covar", "altitude", "course_gnd", "speed_gnd", "num_good_beams", "sound_speed", "beam_ranges_valid", "beam_velocities_valid", "beam_unit_vec", "range", "range_covar", "beam_quality", "beam_velocity", "beam_velocity_covar")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_MODE_FIELD_NUMBER: _ClassVar[int]
    DVL_TYPE_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_COVAR_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    COURSE_GND_FIELD_NUMBER: _ClassVar[int]
    SPEED_GND_FIELD_NUMBER: _ClassVar[int]
    NUM_GOOD_BEAMS_FIELD_NUMBER: _ClassVar[int]
    SOUND_SPEED_FIELD_NUMBER: _ClassVar[int]
    BEAM_RANGES_VALID_FIELD_NUMBER: _ClassVar[int]
    BEAM_VELOCITIES_VALID_FIELD_NUMBER: _ClassVar[int]
    BEAM_UNIT_VEC_FIELD_NUMBER: _ClassVar[int]
    RANGE_FIELD_NUMBER: _ClassVar[int]
    RANGE_COVAR_FIELD_NUMBER: _ClassVar[int]
    BEAM_QUALITY_FIELD_NUMBER: _ClassVar[int]
    BEAM_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    BEAM_VELOCITY_COVAR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    velocity_mode: int
    dvl_type: int
    velocity: _vector3_pb2.Vector3
    velocity_covar: _containers.RepeatedScalarFieldContainer[float]
    altitude: float
    course_gnd: float
    speed_gnd: float
    num_good_beams: int
    sound_speed: float
    beam_ranges_valid: bool
    beam_velocities_valid: bool
    beam_unit_vec: _containers.RepeatedCompositeFieldContainer[_vector3_pb2.Vector3]
    range: _containers.RepeatedScalarFieldContainer[float]
    range_covar: _containers.RepeatedScalarFieldContainer[float]
    beam_quality: _containers.RepeatedScalarFieldContainer[float]
    beam_velocity: _containers.RepeatedScalarFieldContainer[float]
    beam_velocity_covar: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., velocity_mode: _Optional[int] = ..., dvl_type: _Optional[int] = ..., velocity: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., velocity_covar: _Optional[_Iterable[float]] = ..., altitude: _Optional[float] = ..., course_gnd: _Optional[float] = ..., speed_gnd: _Optional[float] = ..., num_good_beams: _Optional[int] = ..., sound_speed: _Optional[float] = ..., beam_ranges_valid: bool = ..., beam_velocities_valid: bool = ..., beam_unit_vec: _Optional[_Iterable[_Union[_vector3_pb2.Vector3, _Mapping]]] = ..., range: _Optional[_Iterable[float]] = ..., range_covar: _Optional[_Iterable[float]] = ..., beam_quality: _Optional[_Iterable[float]] = ..., beam_velocity: _Optional[_Iterable[float]] = ..., beam_velocity_covar: _Optional[_Iterable[float]] = ...) -> None: ...
