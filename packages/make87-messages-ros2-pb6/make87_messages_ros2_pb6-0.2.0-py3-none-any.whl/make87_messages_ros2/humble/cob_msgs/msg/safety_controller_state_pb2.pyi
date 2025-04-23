from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SafetyControllerState(_message.Message):
    __slots__ = ("header", "ros2_header", "has_wireless_emstop", "has_fall_sensors", "has_magnetic_safety_switch", "ack_needed", "emergency_button_stop", "brake_button_stop", "laser_stop", "wireless_stop", "fall_sensor_stop", "external_stop", "laser_bridged", "wireless_bridged", "magnetic_safety_switch", "laser_front_ok", "laser_left_ok", "laser_right_ok", "fall_sensor_front", "fall_sensor_left", "fall_sensor_right", "fall_sensor_released", "base_active", "torso_active", "base_enabled", "torso_enabled")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    HAS_WIRELESS_EMSTOP_FIELD_NUMBER: _ClassVar[int]
    HAS_FALL_SENSORS_FIELD_NUMBER: _ClassVar[int]
    HAS_MAGNETIC_SAFETY_SWITCH_FIELD_NUMBER: _ClassVar[int]
    ACK_NEEDED_FIELD_NUMBER: _ClassVar[int]
    EMERGENCY_BUTTON_STOP_FIELD_NUMBER: _ClassVar[int]
    BRAKE_BUTTON_STOP_FIELD_NUMBER: _ClassVar[int]
    LASER_STOP_FIELD_NUMBER: _ClassVar[int]
    WIRELESS_STOP_FIELD_NUMBER: _ClassVar[int]
    FALL_SENSOR_STOP_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_STOP_FIELD_NUMBER: _ClassVar[int]
    LASER_BRIDGED_FIELD_NUMBER: _ClassVar[int]
    WIRELESS_BRIDGED_FIELD_NUMBER: _ClassVar[int]
    MAGNETIC_SAFETY_SWITCH_FIELD_NUMBER: _ClassVar[int]
    LASER_FRONT_OK_FIELD_NUMBER: _ClassVar[int]
    LASER_LEFT_OK_FIELD_NUMBER: _ClassVar[int]
    LASER_RIGHT_OK_FIELD_NUMBER: _ClassVar[int]
    FALL_SENSOR_FRONT_FIELD_NUMBER: _ClassVar[int]
    FALL_SENSOR_LEFT_FIELD_NUMBER: _ClassVar[int]
    FALL_SENSOR_RIGHT_FIELD_NUMBER: _ClassVar[int]
    FALL_SENSOR_RELEASED_FIELD_NUMBER: _ClassVar[int]
    BASE_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    TORSO_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    BASE_ENABLED_FIELD_NUMBER: _ClassVar[int]
    TORSO_ENABLED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    has_wireless_emstop: bool
    has_fall_sensors: bool
    has_magnetic_safety_switch: bool
    ack_needed: bool
    emergency_button_stop: bool
    brake_button_stop: bool
    laser_stop: bool
    wireless_stop: bool
    fall_sensor_stop: bool
    external_stop: bool
    laser_bridged: bool
    wireless_bridged: bool
    magnetic_safety_switch: bool
    laser_front_ok: bool
    laser_left_ok: bool
    laser_right_ok: bool
    fall_sensor_front: bool
    fall_sensor_left: bool
    fall_sensor_right: bool
    fall_sensor_released: bool
    base_active: bool
    torso_active: bool
    base_enabled: bool
    torso_enabled: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., has_wireless_emstop: bool = ..., has_fall_sensors: bool = ..., has_magnetic_safety_switch: bool = ..., ack_needed: bool = ..., emergency_button_stop: bool = ..., brake_button_stop: bool = ..., laser_stop: bool = ..., wireless_stop: bool = ..., fall_sensor_stop: bool = ..., external_stop: bool = ..., laser_bridged: bool = ..., wireless_bridged: bool = ..., magnetic_safety_switch: bool = ..., laser_front_ok: bool = ..., laser_left_ok: bool = ..., laser_right_ok: bool = ..., fall_sensor_front: bool = ..., fall_sensor_left: bool = ..., fall_sensor_right: bool = ..., fall_sensor_released: bool = ..., base_active: bool = ..., torso_active: bool = ..., base_enabled: bool = ..., torso_enabled: bool = ...) -> None: ...
