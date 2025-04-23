from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ServiceHeader(_message.Message):
    __slots__ = ("header", "stamp", "sequence", "sender", "result")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    stamp: _time_pb2.Time
    sequence: int
    sender: str
    result: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., sequence: _Optional[int] = ..., sender: _Optional[str] = ..., result: bool = ...) -> None: ...
