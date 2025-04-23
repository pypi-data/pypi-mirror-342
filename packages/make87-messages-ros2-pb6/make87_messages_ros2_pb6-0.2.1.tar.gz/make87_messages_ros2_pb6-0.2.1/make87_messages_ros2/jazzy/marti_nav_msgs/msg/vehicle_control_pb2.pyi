from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VehicleControl(_message.Message):
    __slots__ = ("header", "engine", "gear", "steering", "throttle", "brake", "steering_position", "gb_position")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ENGINE_FIELD_NUMBER: _ClassVar[int]
    GEAR_FIELD_NUMBER: _ClassVar[int]
    STEERING_FIELD_NUMBER: _ClassVar[int]
    THROTTLE_FIELD_NUMBER: _ClassVar[int]
    BRAKE_FIELD_NUMBER: _ClassVar[int]
    STEERING_POSITION_FIELD_NUMBER: _ClassVar[int]
    GB_POSITION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    engine: int
    gear: int
    steering: float
    throttle: float
    brake: float
    steering_position: int
    gb_position: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., engine: _Optional[int] = ..., gear: _Optional[int] = ..., steering: _Optional[float] = ..., throttle: _Optional[float] = ..., brake: _Optional[float] = ..., steering_position: _Optional[int] = ..., gb_position: _Optional[int] = ...) -> None: ...
