from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Feedback(_message.Message):
    __slots__ = ("header", "device_number", "device_name", "duty_cycle", "current", "travel", "speed", "setpoint")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DEVICE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    DUTY_CYCLE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_FIELD_NUMBER: _ClassVar[int]
    TRAVEL_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    SETPOINT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    device_number: int
    device_name: str
    duty_cycle: float
    current: float
    travel: float
    speed: float
    setpoint: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., device_number: _Optional[int] = ..., device_name: _Optional[str] = ..., duty_cycle: _Optional[float] = ..., current: _Optional[float] = ..., travel: _Optional[float] = ..., speed: _Optional[float] = ..., setpoint: _Optional[float] = ...) -> None: ...
