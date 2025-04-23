from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EsrStatus2(_message.Message):
    __slots__ = ("header", "canmsg", "maximum_tracks_ack", "rolling_count_2", "overheat_error", "range_perf_error", "internal_error", "xcvr_operational", "raw_data_mode", "steering_angle_ack", "temperature", "veh_spd_comp_factor", "grouping_mode", "yaw_rate_bias", "sw_version_dsp")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CANMSG_FIELD_NUMBER: _ClassVar[int]
    MAXIMUM_TRACKS_ACK_FIELD_NUMBER: _ClassVar[int]
    ROLLING_COUNT_2_FIELD_NUMBER: _ClassVar[int]
    OVERHEAT_ERROR_FIELD_NUMBER: _ClassVar[int]
    RANGE_PERF_ERROR_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_ERROR_FIELD_NUMBER: _ClassVar[int]
    XCVR_OPERATIONAL_FIELD_NUMBER: _ClassVar[int]
    RAW_DATA_MODE_FIELD_NUMBER: _ClassVar[int]
    STEERING_ANGLE_ACK_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    VEH_SPD_COMP_FACTOR_FIELD_NUMBER: _ClassVar[int]
    GROUPING_MODE_FIELD_NUMBER: _ClassVar[int]
    YAW_RATE_BIAS_FIELD_NUMBER: _ClassVar[int]
    SW_VERSION_DSP_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    canmsg: str
    maximum_tracks_ack: int
    rolling_count_2: int
    overheat_error: bool
    range_perf_error: bool
    internal_error: bool
    xcvr_operational: bool
    raw_data_mode: bool
    steering_angle_ack: int
    temperature: int
    veh_spd_comp_factor: float
    grouping_mode: int
    yaw_rate_bias: float
    sw_version_dsp: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., canmsg: _Optional[str] = ..., maximum_tracks_ack: _Optional[int] = ..., rolling_count_2: _Optional[int] = ..., overheat_error: bool = ..., range_perf_error: bool = ..., internal_error: bool = ..., xcvr_operational: bool = ..., raw_data_mode: bool = ..., steering_angle_ack: _Optional[int] = ..., temperature: _Optional[int] = ..., veh_spd_comp_factor: _Optional[float] = ..., grouping_mode: _Optional[int] = ..., yaw_rate_bias: _Optional[float] = ..., sw_version_dsp: _Optional[str] = ...) -> None: ...
