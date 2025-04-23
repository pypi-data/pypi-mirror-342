from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Session(_message.Message):
    __slots__ = ("header", "request_time", "requester_id")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    REQUEST_TIME_FIELD_NUMBER: _ClassVar[int]
    REQUESTER_ID_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    request_time: _time_pb2.Time
    requester_id: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., request_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., requester_id: _Optional[str] = ...) -> None: ...
