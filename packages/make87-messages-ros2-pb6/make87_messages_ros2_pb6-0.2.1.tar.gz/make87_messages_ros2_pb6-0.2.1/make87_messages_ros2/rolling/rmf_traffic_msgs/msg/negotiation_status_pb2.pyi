from make87_messages_ros2.rolling.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NegotiationStatus(_message.Message):
    __slots__ = ("conflict_version", "participants", "start_time", "last_response_time")
    CONFLICT_VERSION_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANTS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    LAST_RESPONSE_TIME_FIELD_NUMBER: _ClassVar[int]
    conflict_version: int
    participants: _containers.RepeatedScalarFieldContainer[int]
    start_time: _time_pb2.Time
    last_response_time: _time_pb2.Time
    def __init__(self, conflict_version: _Optional[int] = ..., participants: _Optional[_Iterable[int]] = ..., start_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., last_response_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ...) -> None: ...
