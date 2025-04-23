from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetPidGainsRequest(_message.Message):
    __slots__ = ("header", "p", "i", "d", "i_clamp", "antiwindup")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    P_FIELD_NUMBER: _ClassVar[int]
    I_FIELD_NUMBER: _ClassVar[int]
    D_FIELD_NUMBER: _ClassVar[int]
    I_CLAMP_FIELD_NUMBER: _ClassVar[int]
    ANTIWINDUP_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    p: float
    i: float
    d: float
    i_clamp: float
    antiwindup: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., p: _Optional[float] = ..., i: _Optional[float] = ..., d: _Optional[float] = ..., i_clamp: _Optional[float] = ..., antiwindup: bool = ...) -> None: ...

class SetPidGainsResponse(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...
