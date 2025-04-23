from make87_messages_ros2.rolling.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Clock(_message.Message):
    __slots__ = ("clock",)
    CLOCK_FIELD_NUMBER: _ClassVar[int]
    clock: _time_pb2.Time
    def __init__(self, clock: _Optional[_Union[_time_pb2.Time, _Mapping]] = ...) -> None: ...
