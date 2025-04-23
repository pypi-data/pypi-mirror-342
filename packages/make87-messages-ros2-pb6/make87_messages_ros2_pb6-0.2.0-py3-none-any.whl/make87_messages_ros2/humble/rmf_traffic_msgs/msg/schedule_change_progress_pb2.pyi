from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScheduleChangeProgress(_message.Message):
    __slots__ = ("header", "has_progress", "version", "checkpoints")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    HAS_PROGRESS_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    CHECKPOINTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    has_progress: bool
    version: int
    checkpoints: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., has_progress: bool = ..., version: _Optional[int] = ..., checkpoints: _Optional[_Iterable[int]] = ...) -> None: ...
