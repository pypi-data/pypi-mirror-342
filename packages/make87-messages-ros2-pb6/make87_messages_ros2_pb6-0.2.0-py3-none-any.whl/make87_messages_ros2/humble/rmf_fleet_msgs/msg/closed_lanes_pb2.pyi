from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClosedLanes(_message.Message):
    __slots__ = ("header", "fleet_name", "closed_lanes")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FLEET_NAME_FIELD_NUMBER: _ClassVar[int]
    CLOSED_LANES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    fleet_name: str
    closed_lanes: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., fleet_name: _Optional[str] = ..., closed_lanes: _Optional[_Iterable[int]] = ...) -> None: ...
