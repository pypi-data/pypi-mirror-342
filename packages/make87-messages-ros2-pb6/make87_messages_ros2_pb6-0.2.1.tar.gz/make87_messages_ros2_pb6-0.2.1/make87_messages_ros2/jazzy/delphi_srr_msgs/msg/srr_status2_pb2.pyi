from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SrrStatus2(_message.Message):
    __slots__ = ("header", "can_tx_alignment_status", "can_tx_comm_error", "can_tx_steering_angle_sign", "can_tx_yaw_rate_bias", "can_tx_veh_spd_comp_factor", "can_tx_sw_version_dsp", "can_tx_temperature", "can_tx_range_perf_error", "can_tx_overheat_error", "can_tx_internal_error", "can_tx_xcvr_operational", "can_tx_steering_angle", "can_tx_rolling_count_2")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_ALIGNMENT_STATUS_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_COMM_ERROR_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_STEERING_ANGLE_SIGN_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_YAW_RATE_BIAS_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_VEH_SPD_COMP_FACTOR_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_SW_VERSION_DSP_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_RANGE_PERF_ERROR_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_OVERHEAT_ERROR_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_INTERNAL_ERROR_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_XCVR_OPERATIONAL_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_STEERING_ANGLE_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_ROLLING_COUNT_2_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    can_tx_alignment_status: int
    can_tx_comm_error: bool
    can_tx_steering_angle_sign: bool
    can_tx_yaw_rate_bias: float
    can_tx_veh_spd_comp_factor: float
    can_tx_sw_version_dsp: int
    can_tx_temperature: int
    can_tx_range_perf_error: bool
    can_tx_overheat_error: bool
    can_tx_internal_error: bool
    can_tx_xcvr_operational: bool
    can_tx_steering_angle: int
    can_tx_rolling_count_2: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., can_tx_alignment_status: _Optional[int] = ..., can_tx_comm_error: bool = ..., can_tx_steering_angle_sign: bool = ..., can_tx_yaw_rate_bias: _Optional[float] = ..., can_tx_veh_spd_comp_factor: _Optional[float] = ..., can_tx_sw_version_dsp: _Optional[int] = ..., can_tx_temperature: _Optional[int] = ..., can_tx_range_perf_error: bool = ..., can_tx_overheat_error: bool = ..., can_tx_internal_error: bool = ..., can_tx_xcvr_operational: bool = ..., can_tx_steering_angle: _Optional[int] = ..., can_tx_rolling_count_2: _Optional[int] = ...) -> None: ...
