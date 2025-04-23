from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VehicleStateMsg2(_message.Message):
    __slots__ = ("header", "fsm_yaw_rate_valid", "fsm_yaw_rate", "can_vehicle_index_4fa", "fsm_vehicle_velocity", "can_steering_whl_angle_qf", "fsm_vehicle_velocity_valid", "can_steering_whl_angle")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FSM_YAW_RATE_VALID_FIELD_NUMBER: _ClassVar[int]
    FSM_YAW_RATE_FIELD_NUMBER: _ClassVar[int]
    CAN_VEHICLE_INDEX_4FA_FIELD_NUMBER: _ClassVar[int]
    FSM_VEHICLE_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    CAN_STEERING_WHL_ANGLE_QF_FIELD_NUMBER: _ClassVar[int]
    FSM_VEHICLE_VELOCITY_VALID_FIELD_NUMBER: _ClassVar[int]
    CAN_STEERING_WHL_ANGLE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    fsm_yaw_rate_valid: bool
    fsm_yaw_rate: float
    can_vehicle_index_4fa: int
    fsm_vehicle_velocity: float
    can_steering_whl_angle_qf: bool
    fsm_vehicle_velocity_valid: bool
    can_steering_whl_angle: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., fsm_yaw_rate_valid: bool = ..., fsm_yaw_rate: _Optional[float] = ..., can_vehicle_index_4fa: _Optional[int] = ..., fsm_vehicle_velocity: _Optional[float] = ..., can_steering_whl_angle_qf: bool = ..., fsm_vehicle_velocity_valid: bool = ..., can_steering_whl_angle: _Optional[float] = ...) -> None: ...
