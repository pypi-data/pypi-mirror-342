from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import duration_pb2 as _duration_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BidNotice(_message.Message):
    __slots__ = ("header", "request", "task_id", "time_window")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    TIME_WINDOW_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    request: str
    task_id: str
    time_window: _duration_pb2.Duration
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., request: _Optional[str] = ..., task_id: _Optional[str] = ..., time_window: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...
