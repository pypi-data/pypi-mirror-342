from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.jazzy.ibeo_msgs.msg import ibeo_data_header_pb2 as _ibeo_data_header_pb2
from make87_messages_ros2.jazzy.ibeo_msgs.msg import scan_point2202_pb2 as _scan_point2202_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScanData2202(_message.Message):
    __slots__ = ("header", "ibeo_header", "scan_number", "scanner_status", "sync_phase_offset", "scan_start_time", "scan_end_time", "angle_ticks_per_rotation", "start_angle_ticks", "end_angle_ticks", "scan_points_count", "mounting_yaw_angle_ticks", "mounting_pitch_angle_ticks", "mounting_roll_angle_ticks", "mounting_position_x", "mounting_position_y", "mounting_position_z", "ground_labeled", "dirt_labeled", "rain_labeled", "mirror_side", "scan_point_list")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    IBEO_HEADER_FIELD_NUMBER: _ClassVar[int]
    SCAN_NUMBER_FIELD_NUMBER: _ClassVar[int]
    SCANNER_STATUS_FIELD_NUMBER: _ClassVar[int]
    SYNC_PHASE_OFFSET_FIELD_NUMBER: _ClassVar[int]
    SCAN_START_TIME_FIELD_NUMBER: _ClassVar[int]
    SCAN_END_TIME_FIELD_NUMBER: _ClassVar[int]
    ANGLE_TICKS_PER_ROTATION_FIELD_NUMBER: _ClassVar[int]
    START_ANGLE_TICKS_FIELD_NUMBER: _ClassVar[int]
    END_ANGLE_TICKS_FIELD_NUMBER: _ClassVar[int]
    SCAN_POINTS_COUNT_FIELD_NUMBER: _ClassVar[int]
    MOUNTING_YAW_ANGLE_TICKS_FIELD_NUMBER: _ClassVar[int]
    MOUNTING_PITCH_ANGLE_TICKS_FIELD_NUMBER: _ClassVar[int]
    MOUNTING_ROLL_ANGLE_TICKS_FIELD_NUMBER: _ClassVar[int]
    MOUNTING_POSITION_X_FIELD_NUMBER: _ClassVar[int]
    MOUNTING_POSITION_Y_FIELD_NUMBER: _ClassVar[int]
    MOUNTING_POSITION_Z_FIELD_NUMBER: _ClassVar[int]
    GROUND_LABELED_FIELD_NUMBER: _ClassVar[int]
    DIRT_LABELED_FIELD_NUMBER: _ClassVar[int]
    RAIN_LABELED_FIELD_NUMBER: _ClassVar[int]
    MIRROR_SIDE_FIELD_NUMBER: _ClassVar[int]
    SCAN_POINT_LIST_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ibeo_header: _ibeo_data_header_pb2.IbeoDataHeader
    scan_number: int
    scanner_status: int
    sync_phase_offset: int
    scan_start_time: _time_pb2.Time
    scan_end_time: _time_pb2.Time
    angle_ticks_per_rotation: int
    start_angle_ticks: int
    end_angle_ticks: int
    scan_points_count: int
    mounting_yaw_angle_ticks: int
    mounting_pitch_angle_ticks: int
    mounting_roll_angle_ticks: int
    mounting_position_x: int
    mounting_position_y: int
    mounting_position_z: int
    ground_labeled: bool
    dirt_labeled: bool
    rain_labeled: bool
    mirror_side: int
    scan_point_list: _containers.RepeatedCompositeFieldContainer[_scan_point2202_pb2.ScanPoint2202]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ibeo_header: _Optional[_Union[_ibeo_data_header_pb2.IbeoDataHeader, _Mapping]] = ..., scan_number: _Optional[int] = ..., scanner_status: _Optional[int] = ..., sync_phase_offset: _Optional[int] = ..., scan_start_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., scan_end_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., angle_ticks_per_rotation: _Optional[int] = ..., start_angle_ticks: _Optional[int] = ..., end_angle_ticks: _Optional[int] = ..., scan_points_count: _Optional[int] = ..., mounting_yaw_angle_ticks: _Optional[int] = ..., mounting_pitch_angle_ticks: _Optional[int] = ..., mounting_roll_angle_ticks: _Optional[int] = ..., mounting_position_x: _Optional[int] = ..., mounting_position_y: _Optional[int] = ..., mounting_position_z: _Optional[int] = ..., ground_labeled: bool = ..., dirt_labeled: bool = ..., rain_labeled: bool = ..., mirror_side: _Optional[int] = ..., scan_point_list: _Optional[_Iterable[_Union[_scan_point2202_pb2.ScanPoint2202, _Mapping]]] = ...) -> None: ...
