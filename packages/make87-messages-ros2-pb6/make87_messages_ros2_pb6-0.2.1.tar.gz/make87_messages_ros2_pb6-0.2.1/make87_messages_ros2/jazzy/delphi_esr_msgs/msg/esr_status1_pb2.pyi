from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EsrStatus1(_message.Message):
    __slots__ = ("header", "canmsg", "rolling_count_1", "dsp_timestamp", "comm_error", "radius_curvature_calc", "scan_index", "yaw_rate_calc", "vehicle_speed_calc")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CANMSG_FIELD_NUMBER: _ClassVar[int]
    ROLLING_COUNT_1_FIELD_NUMBER: _ClassVar[int]
    DSP_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    COMM_ERROR_FIELD_NUMBER: _ClassVar[int]
    RADIUS_CURVATURE_CALC_FIELD_NUMBER: _ClassVar[int]
    SCAN_INDEX_FIELD_NUMBER: _ClassVar[int]
    YAW_RATE_CALC_FIELD_NUMBER: _ClassVar[int]
    VEHICLE_SPEED_CALC_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    canmsg: str
    rolling_count_1: int
    dsp_timestamp: int
    comm_error: bool
    radius_curvature_calc: int
    scan_index: int
    yaw_rate_calc: float
    vehicle_speed_calc: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., canmsg: _Optional[str] = ..., rolling_count_1: _Optional[int] = ..., dsp_timestamp: _Optional[int] = ..., comm_error: bool = ..., radius_curvature_calc: _Optional[int] = ..., scan_index: _Optional[int] = ..., yaw_rate_calc: _Optional[float] = ..., vehicle_speed_calc: _Optional[float] = ...) -> None: ...
