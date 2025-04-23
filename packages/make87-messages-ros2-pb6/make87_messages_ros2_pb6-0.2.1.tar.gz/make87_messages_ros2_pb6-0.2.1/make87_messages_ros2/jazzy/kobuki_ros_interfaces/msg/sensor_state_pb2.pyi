from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SensorState(_message.Message):
    __slots__ = ("header", "time_stamp", "bumper", "wheel_drop", "cliff", "left_encoder", "right_encoder", "left_pwm", "right_pwm", "buttons", "charger", "battery", "bottom", "current", "over_current", "digital_input", "analog_input")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TIME_STAMP_FIELD_NUMBER: _ClassVar[int]
    BUMPER_FIELD_NUMBER: _ClassVar[int]
    WHEEL_DROP_FIELD_NUMBER: _ClassVar[int]
    CLIFF_FIELD_NUMBER: _ClassVar[int]
    LEFT_ENCODER_FIELD_NUMBER: _ClassVar[int]
    RIGHT_ENCODER_FIELD_NUMBER: _ClassVar[int]
    LEFT_PWM_FIELD_NUMBER: _ClassVar[int]
    RIGHT_PWM_FIELD_NUMBER: _ClassVar[int]
    BUTTONS_FIELD_NUMBER: _ClassVar[int]
    CHARGER_FIELD_NUMBER: _ClassVar[int]
    BATTERY_FIELD_NUMBER: _ClassVar[int]
    BOTTOM_FIELD_NUMBER: _ClassVar[int]
    CURRENT_FIELD_NUMBER: _ClassVar[int]
    OVER_CURRENT_FIELD_NUMBER: _ClassVar[int]
    DIGITAL_INPUT_FIELD_NUMBER: _ClassVar[int]
    ANALOG_INPUT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    time_stamp: int
    bumper: int
    wheel_drop: int
    cliff: int
    left_encoder: int
    right_encoder: int
    left_pwm: int
    right_pwm: int
    buttons: int
    charger: int
    battery: int
    bottom: _containers.RepeatedScalarFieldContainer[int]
    current: _containers.RepeatedScalarFieldContainer[int]
    over_current: int
    digital_input: int
    analog_input: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., time_stamp: _Optional[int] = ..., bumper: _Optional[int] = ..., wheel_drop: _Optional[int] = ..., cliff: _Optional[int] = ..., left_encoder: _Optional[int] = ..., right_encoder: _Optional[int] = ..., left_pwm: _Optional[int] = ..., right_pwm: _Optional[int] = ..., buttons: _Optional[int] = ..., charger: _Optional[int] = ..., battery: _Optional[int] = ..., bottom: _Optional[_Iterable[int]] = ..., current: _Optional[_Iterable[int]] = ..., over_current: _Optional[int] = ..., digital_input: _Optional[int] = ..., analog_input: _Optional[_Iterable[int]] = ...) -> None: ...
