from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TestSubArray(_message.Message):
    __slots__ = ("ints", "strings", "times")
    INTS_FIELD_NUMBER: _ClassVar[int]
    STRINGS_FIELD_NUMBER: _ClassVar[int]
    TIMES_FIELD_NUMBER: _ClassVar[int]
    ints: _containers.RepeatedScalarFieldContainer[int]
    strings: _containers.RepeatedScalarFieldContainer[str]
    times: _containers.RepeatedCompositeFieldContainer[_time_pb2.Time]
    def __init__(self, ints: _Optional[_Iterable[int]] = ..., strings: _Optional[_Iterable[str]] = ..., times: _Optional[_Iterable[_Union[_time_pb2.Time, _Mapping]]] = ...) -> None: ...
