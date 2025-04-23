from make87_messages_ros2.jazzy.builtin_interfaces.msg import duration_pb2 as _duration_pb2
from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Button(_message.Message):
    __slots__ = ("header", "is_pressed", "last_start_pressed_time", "last_pressed_duration")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    IS_PRESSED_FIELD_NUMBER: _ClassVar[int]
    LAST_START_PRESSED_TIME_FIELD_NUMBER: _ClassVar[int]
    LAST_PRESSED_DURATION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    is_pressed: bool
    last_start_pressed_time: _time_pb2.Time
    last_pressed_duration: _duration_pb2.Duration
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., is_pressed: bool = ..., last_start_pressed_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., last_pressed_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...
