from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DispatchCommand(_message.Message):
    __slots__ = ("header", "fleet_name", "task_id", "dispatch_id", "timestamp", "type")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FLEET_NAME_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    DISPATCH_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    fleet_name: str
    task_id: str
    dispatch_id: int
    timestamp: _time_pb2.Time
    type: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., fleet_name: _Optional[str] = ..., task_id: _Optional[str] = ..., dispatch_id: _Optional[int] = ..., timestamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., type: _Optional[int] = ...) -> None: ...
