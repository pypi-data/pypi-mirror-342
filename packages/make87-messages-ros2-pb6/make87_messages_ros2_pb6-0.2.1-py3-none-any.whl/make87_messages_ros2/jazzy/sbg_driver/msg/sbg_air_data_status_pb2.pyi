from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SbgAirDataStatus(_message.Message):
    __slots__ = ("is_delay_time", "pressure_valid", "altitude_valid", "pressure_diff_valid", "air_speed_valid", "air_temperature_valid")
    IS_DELAY_TIME_FIELD_NUMBER: _ClassVar[int]
    PRESSURE_VALID_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_VALID_FIELD_NUMBER: _ClassVar[int]
    PRESSURE_DIFF_VALID_FIELD_NUMBER: _ClassVar[int]
    AIR_SPEED_VALID_FIELD_NUMBER: _ClassVar[int]
    AIR_TEMPERATURE_VALID_FIELD_NUMBER: _ClassVar[int]
    is_delay_time: bool
    pressure_valid: bool
    altitude_valid: bool
    pressure_diff_valid: bool
    air_speed_valid: bool
    air_temperature_valid: bool
    def __init__(self, is_delay_time: bool = ..., pressure_valid: bool = ..., altitude_valid: bool = ..., pressure_diff_valid: bool = ..., air_speed_valid: bool = ..., air_temperature_valid: bool = ...) -> None: ...
