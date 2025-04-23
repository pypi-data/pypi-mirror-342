from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Hear(_message.Message):
    __slots__ = ("header", "team", "time", "self", "direction", "message")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TEAM_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    SELF_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    team: str
    time: float
    self: bool
    direction: _containers.RepeatedScalarFieldContainer[float]
    message: str
    def __init__(self_, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., team: _Optional[str] = ..., time: _Optional[float] = ..., self: bool = ..., direction: _Optional[_Iterable[float]] = ..., message: _Optional[str] = ...) -> None: ...
