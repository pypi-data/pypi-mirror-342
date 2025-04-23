from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StatusEvent(_message.Message):
    __slots__ = ("header", "severity", "px4_id", "arguments", "sequence")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    PX4_ID_FIELD_NUMBER: _ClassVar[int]
    ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    severity: int
    px4_id: int
    arguments: _containers.RepeatedScalarFieldContainer[int]
    sequence: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., severity: _Optional[int] = ..., px4_id: _Optional[int] = ..., arguments: _Optional[_Iterable[int]] = ..., sequence: _Optional[int] = ...) -> None: ...
