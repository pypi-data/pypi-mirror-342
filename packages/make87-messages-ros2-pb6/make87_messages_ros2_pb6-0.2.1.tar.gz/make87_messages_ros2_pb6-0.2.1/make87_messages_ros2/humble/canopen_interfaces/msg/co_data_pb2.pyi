from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class COData(_message.Message):
    __slots__ = ("header", "index", "subindex", "data")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    SUBINDEX_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    index: int
    subindex: int
    data: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., index: _Optional[int] = ..., subindex: _Optional[int] = ..., data: _Optional[int] = ...) -> None: ...
