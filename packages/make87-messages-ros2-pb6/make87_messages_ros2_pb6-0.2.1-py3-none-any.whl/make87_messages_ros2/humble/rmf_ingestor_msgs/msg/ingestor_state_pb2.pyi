from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IngestorState(_message.Message):
    __slots__ = ("header", "time", "guid", "mode", "request_guid_queue", "seconds_remaining")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    GUID_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_GUID_QUEUE_FIELD_NUMBER: _ClassVar[int]
    SECONDS_REMAINING_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    time: _time_pb2.Time
    guid: str
    mode: int
    request_guid_queue: _containers.RepeatedScalarFieldContainer[str]
    seconds_remaining: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., guid: _Optional[str] = ..., mode: _Optional[int] = ..., request_guid_queue: _Optional[_Iterable[str]] = ..., seconds_remaining: _Optional[float] = ...) -> None: ...
