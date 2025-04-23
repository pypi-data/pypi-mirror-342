from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PlanItem(_message.Message):
    __slots__ = ("header", "time", "action", "duration")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    time: float
    action: str
    duration: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., time: _Optional[float] = ..., action: _Optional[str] = ..., duration: _Optional[float] = ...) -> None: ...
