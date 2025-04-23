from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PathPlanning(_message.Message):
    __slots__ = ("header", "segment_type", "length", "start_speed", "end_speed", "startx", "starty", "endx", "endy", "theta0", "a1", "a2", "k0", "c1", "c2", "behavior", "creep", "acc", "reverse", "vehicle_track", "transmitted", "aux_transmitted", "theta_end", "k_end", "seg_len", "speed_limit", "max_error", "max_smooth", "max_curv", "possible_points", "exit_segment")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    START_SPEED_FIELD_NUMBER: _ClassVar[int]
    END_SPEED_FIELD_NUMBER: _ClassVar[int]
    STARTX_FIELD_NUMBER: _ClassVar[int]
    STARTY_FIELD_NUMBER: _ClassVar[int]
    ENDX_FIELD_NUMBER: _ClassVar[int]
    ENDY_FIELD_NUMBER: _ClassVar[int]
    THETA0_FIELD_NUMBER: _ClassVar[int]
    A1_FIELD_NUMBER: _ClassVar[int]
    A2_FIELD_NUMBER: _ClassVar[int]
    K0_FIELD_NUMBER: _ClassVar[int]
    C1_FIELD_NUMBER: _ClassVar[int]
    C2_FIELD_NUMBER: _ClassVar[int]
    BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    CREEP_FIELD_NUMBER: _ClassVar[int]
    ACC_FIELD_NUMBER: _ClassVar[int]
    REVERSE_FIELD_NUMBER: _ClassVar[int]
    VEHICLE_TRACK_FIELD_NUMBER: _ClassVar[int]
    TRANSMITTED_FIELD_NUMBER: _ClassVar[int]
    AUX_TRANSMITTED_FIELD_NUMBER: _ClassVar[int]
    THETA_END_FIELD_NUMBER: _ClassVar[int]
    K_END_FIELD_NUMBER: _ClassVar[int]
    SEG_LEN_FIELD_NUMBER: _ClassVar[int]
    SPEED_LIMIT_FIELD_NUMBER: _ClassVar[int]
    MAX_ERROR_FIELD_NUMBER: _ClassVar[int]
    MAX_SMOOTH_FIELD_NUMBER: _ClassVar[int]
    MAX_CURV_FIELD_NUMBER: _ClassVar[int]
    POSSIBLE_POINTS_FIELD_NUMBER: _ClassVar[int]
    EXIT_SEGMENT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    segment_type: int
    length: float
    start_speed: float
    end_speed: float
    startx: float
    starty: float
    endx: float
    endy: float
    theta0: float
    a1: float
    a2: float
    k0: float
    c1: float
    c2: float
    behavior: int
    creep: int
    acc: int
    reverse: int
    vehicle_track: int
    transmitted: bool
    aux_transmitted: bool
    theta_end: float
    k_end: float
    seg_len: int
    speed_limit: float
    max_error: float
    max_smooth: float
    max_curv: float
    possible_points: int
    exit_segment: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., segment_type: _Optional[int] = ..., length: _Optional[float] = ..., start_speed: _Optional[float] = ..., end_speed: _Optional[float] = ..., startx: _Optional[float] = ..., starty: _Optional[float] = ..., endx: _Optional[float] = ..., endy: _Optional[float] = ..., theta0: _Optional[float] = ..., a1: _Optional[float] = ..., a2: _Optional[float] = ..., k0: _Optional[float] = ..., c1: _Optional[float] = ..., c2: _Optional[float] = ..., behavior: _Optional[int] = ..., creep: _Optional[int] = ..., acc: _Optional[int] = ..., reverse: _Optional[int] = ..., vehicle_track: _Optional[int] = ..., transmitted: bool = ..., aux_transmitted: bool = ..., theta_end: _Optional[float] = ..., k_end: _Optional[float] = ..., seg_len: _Optional[int] = ..., speed_limit: _Optional[float] = ..., max_error: _Optional[float] = ..., max_smooth: _Optional[float] = ..., max_curv: _Optional[float] = ..., possible_points: _Optional[int] = ..., exit_segment: bool = ...) -> None: ...
