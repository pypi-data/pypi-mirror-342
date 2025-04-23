from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetPenRequest(_message.Message):
    __slots__ = ("header", "r", "g", "b", "width", "off")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    R_FIELD_NUMBER: _ClassVar[int]
    G_FIELD_NUMBER: _ClassVar[int]
    B_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    OFF_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    r: int
    g: int
    b: int
    width: int
    off: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., r: _Optional[int] = ..., g: _Optional[int] = ..., b: _Optional[int] = ..., width: _Optional[int] = ..., off: _Optional[int] = ...) -> None: ...

class SetPenResponse(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...
