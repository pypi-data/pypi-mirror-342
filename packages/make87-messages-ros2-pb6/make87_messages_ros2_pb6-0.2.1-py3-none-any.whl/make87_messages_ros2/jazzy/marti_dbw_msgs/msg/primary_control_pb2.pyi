from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PrimaryControl(_message.Message):
    __slots__ = ("header", "active", "estop", "steering_command", "throttle_command", "brake_command")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    ESTOP_FIELD_NUMBER: _ClassVar[int]
    STEERING_COMMAND_FIELD_NUMBER: _ClassVar[int]
    THROTTLE_COMMAND_FIELD_NUMBER: _ClassVar[int]
    BRAKE_COMMAND_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    active: bool
    estop: bool
    steering_command: float
    throttle_command: float
    brake_command: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., active: bool = ..., estop: bool = ..., steering_command: _Optional[float] = ..., throttle_command: _Optional[float] = ..., brake_command: _Optional[float] = ...) -> None: ...
