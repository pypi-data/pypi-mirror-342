from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import duration_pb2 as _duration_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TestDurationArray(_message.Message):
    __slots__ = ("header", "durations")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DURATIONS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    durations: _containers.RepeatedCompositeFieldContainer[_duration_pb2.Duration]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., durations: _Optional[_Iterable[_Union[_duration_pb2.Duration, _Mapping]]] = ...) -> None: ...
