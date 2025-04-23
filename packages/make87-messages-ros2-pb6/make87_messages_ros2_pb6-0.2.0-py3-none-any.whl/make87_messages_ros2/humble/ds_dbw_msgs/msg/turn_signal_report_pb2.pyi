from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.ds_dbw_msgs.msg import turn_signal_pb2 as _turn_signal_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TurnSignalReport(_message.Message):
    __slots__ = ("header", "ros2_header", "input", "cmd", "output", "feedback", "ready", "override_active", "override_other", "timeout", "bad_crc", "bad_rc", "degraded", "degraded_cmd_type", "degraded_comms_dbw_steer", "degraded_comms_dbw_brake", "degraded_comms_dbw_thrtl", "degraded_comms_vehicle", "degraded_control_performance", "fault", "fault_comms_vehicle")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    CMD_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    FEEDBACK_FIELD_NUMBER: _ClassVar[int]
    READY_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_OTHER_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    BAD_CRC_FIELD_NUMBER: _ClassVar[int]
    BAD_RC_FIELD_NUMBER: _ClassVar[int]
    DEGRADED_FIELD_NUMBER: _ClassVar[int]
    DEGRADED_CMD_TYPE_FIELD_NUMBER: _ClassVar[int]
    DEGRADED_COMMS_DBW_STEER_FIELD_NUMBER: _ClassVar[int]
    DEGRADED_COMMS_DBW_BRAKE_FIELD_NUMBER: _ClassVar[int]
    DEGRADED_COMMS_DBW_THRTL_FIELD_NUMBER: _ClassVar[int]
    DEGRADED_COMMS_VEHICLE_FIELD_NUMBER: _ClassVar[int]
    DEGRADED_CONTROL_PERFORMANCE_FIELD_NUMBER: _ClassVar[int]
    FAULT_FIELD_NUMBER: _ClassVar[int]
    FAULT_COMMS_VEHICLE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    input: _turn_signal_pb2.TurnSignal
    cmd: _turn_signal_pb2.TurnSignal
    output: _turn_signal_pb2.TurnSignal
    feedback: _turn_signal_pb2.TurnSignal
    ready: bool
    override_active: bool
    override_other: bool
    timeout: bool
    bad_crc: bool
    bad_rc: bool
    degraded: bool
    degraded_cmd_type: bool
    degraded_comms_dbw_steer: bool
    degraded_comms_dbw_brake: bool
    degraded_comms_dbw_thrtl: bool
    degraded_comms_vehicle: bool
    degraded_control_performance: bool
    fault: bool
    fault_comms_vehicle: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., input: _Optional[_Union[_turn_signal_pb2.TurnSignal, _Mapping]] = ..., cmd: _Optional[_Union[_turn_signal_pb2.TurnSignal, _Mapping]] = ..., output: _Optional[_Union[_turn_signal_pb2.TurnSignal, _Mapping]] = ..., feedback: _Optional[_Union[_turn_signal_pb2.TurnSignal, _Mapping]] = ..., ready: bool = ..., override_active: bool = ..., override_other: bool = ..., timeout: bool = ..., bad_crc: bool = ..., bad_rc: bool = ..., degraded: bool = ..., degraded_cmd_type: bool = ..., degraded_comms_dbw_steer: bool = ..., degraded_comms_dbw_brake: bool = ..., degraded_comms_dbw_thrtl: bool = ..., degraded_comms_vehicle: bool = ..., degraded_control_performance: bool = ..., fault: bool = ..., fault_comms_vehicle: bool = ...) -> None: ...
