from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NovatelPsrdop2System(_message.Message):
    __slots__ = ("header", "system", "tdop")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_FIELD_NUMBER: _ClassVar[int]
    TDOP_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    system: str
    tdop: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., system: _Optional[str] = ..., tdop: _Optional[float] = ...) -> None: ...
