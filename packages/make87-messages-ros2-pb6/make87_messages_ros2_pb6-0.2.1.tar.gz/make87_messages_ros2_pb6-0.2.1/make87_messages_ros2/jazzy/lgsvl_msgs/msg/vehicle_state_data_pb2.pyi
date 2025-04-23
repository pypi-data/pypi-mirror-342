from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VehicleStateData(_message.Message):
    __slots__ = ("header", "blinker_state", "headlight_state", "wiper_state", "current_gear", "vehicle_mode", "hand_brake_active", "horn_active", "autonomous_mode_active")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BLINKER_STATE_FIELD_NUMBER: _ClassVar[int]
    HEADLIGHT_STATE_FIELD_NUMBER: _ClassVar[int]
    WIPER_STATE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_GEAR_FIELD_NUMBER: _ClassVar[int]
    VEHICLE_MODE_FIELD_NUMBER: _ClassVar[int]
    HAND_BRAKE_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    HORN_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    AUTONOMOUS_MODE_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    blinker_state: int
    headlight_state: int
    wiper_state: int
    current_gear: int
    vehicle_mode: int
    hand_brake_active: bool
    horn_active: bool
    autonomous_mode_active: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., blinker_state: _Optional[int] = ..., headlight_state: _Optional[int] = ..., wiper_state: _Optional[int] = ..., current_gear: _Optional[int] = ..., vehicle_mode: _Optional[int] = ..., hand_brake_active: bool = ..., horn_active: bool = ..., autonomous_mode_active: bool = ...) -> None: ...
