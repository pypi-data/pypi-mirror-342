from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Size2D(_message.Message):
    __slots__ = ("header", "size_x", "size_y")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SIZE_X_FIELD_NUMBER: _ClassVar[int]
    SIZE_Y_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    size_x: int
    size_y: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., size_x: _Optional[int] = ..., size_y: _Optional[int] = ...) -> None: ...
