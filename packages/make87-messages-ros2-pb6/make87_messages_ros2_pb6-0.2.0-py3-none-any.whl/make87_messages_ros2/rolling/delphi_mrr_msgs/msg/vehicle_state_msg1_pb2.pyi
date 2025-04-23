from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VehicleStateMsg1(_message.Message):
    __slots__ = ("header", "can_fcw_sensitivity_level", "can_vehicle_stationary", "can_intf_minor_version", "can_intf_major_version", "can_brake_pedal", "can_high_wheel_slip", "can_turn_signal_status", "can_washer_front_cmd", "can_wiper_front_cmd", "can_wiper_speed_info", "can_reverse_gear", "can_beam_shape_actual_right", "can_beam_shape_actual_left", "can_main_beam_indication", "can_vehicle_index")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CAN_FCW_SENSITIVITY_LEVEL_FIELD_NUMBER: _ClassVar[int]
    CAN_VEHICLE_STATIONARY_FIELD_NUMBER: _ClassVar[int]
    CAN_INTF_MINOR_VERSION_FIELD_NUMBER: _ClassVar[int]
    CAN_INTF_MAJOR_VERSION_FIELD_NUMBER: _ClassVar[int]
    CAN_BRAKE_PEDAL_FIELD_NUMBER: _ClassVar[int]
    CAN_HIGH_WHEEL_SLIP_FIELD_NUMBER: _ClassVar[int]
    CAN_TURN_SIGNAL_STATUS_FIELD_NUMBER: _ClassVar[int]
    CAN_WASHER_FRONT_CMD_FIELD_NUMBER: _ClassVar[int]
    CAN_WIPER_FRONT_CMD_FIELD_NUMBER: _ClassVar[int]
    CAN_WIPER_SPEED_INFO_FIELD_NUMBER: _ClassVar[int]
    CAN_REVERSE_GEAR_FIELD_NUMBER: _ClassVar[int]
    CAN_BEAM_SHAPE_ACTUAL_RIGHT_FIELD_NUMBER: _ClassVar[int]
    CAN_BEAM_SHAPE_ACTUAL_LEFT_FIELD_NUMBER: _ClassVar[int]
    CAN_MAIN_BEAM_INDICATION_FIELD_NUMBER: _ClassVar[int]
    CAN_VEHICLE_INDEX_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    can_fcw_sensitivity_level: int
    can_vehicle_stationary: bool
    can_intf_minor_version: int
    can_intf_major_version: int
    can_brake_pedal: int
    can_high_wheel_slip: bool
    can_turn_signal_status: int
    can_washer_front_cmd: bool
    can_wiper_front_cmd: bool
    can_wiper_speed_info: int
    can_reverse_gear: bool
    can_beam_shape_actual_right: int
    can_beam_shape_actual_left: int
    can_main_beam_indication: bool
    can_vehicle_index: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., can_fcw_sensitivity_level: _Optional[int] = ..., can_vehicle_stationary: bool = ..., can_intf_minor_version: _Optional[int] = ..., can_intf_major_version: _Optional[int] = ..., can_brake_pedal: _Optional[int] = ..., can_high_wheel_slip: bool = ..., can_turn_signal_status: _Optional[int] = ..., can_washer_front_cmd: bool = ..., can_wiper_front_cmd: bool = ..., can_wiper_speed_info: _Optional[int] = ..., can_reverse_gear: bool = ..., can_beam_shape_actual_right: _Optional[int] = ..., can_beam_shape_actual_left: _Optional[int] = ..., can_main_beam_indication: bool = ..., can_vehicle_index: _Optional[int] = ...) -> None: ...
