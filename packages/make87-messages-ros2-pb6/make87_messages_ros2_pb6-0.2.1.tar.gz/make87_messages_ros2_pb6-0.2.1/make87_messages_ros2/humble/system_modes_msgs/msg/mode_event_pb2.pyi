from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.system_modes_msgs.msg import mode_pb2 as _mode_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ModeEvent(_message.Message):
    __slots__ = ("header", "timestamp", "start_mode", "goal_mode")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    START_MODE_FIELD_NUMBER: _ClassVar[int]
    GOAL_MODE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    timestamp: int
    start_mode: _mode_pb2.Mode
    goal_mode: _mode_pb2.Mode
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., timestamp: _Optional[int] = ..., start_mode: _Optional[_Union[_mode_pb2.Mode, _Mapping]] = ..., goal_mode: _Optional[_Union[_mode_pb2.Mode, _Mapping]] = ...) -> None: ...
