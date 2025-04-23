from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TopicsAndRawTypesRequest(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class TopicsAndRawTypesResponse(_message.Message):
    __slots__ = ("header", "topics", "types", "typedefs_full_text")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TOPICS_FIELD_NUMBER: _ClassVar[int]
    TYPES_FIELD_NUMBER: _ClassVar[int]
    TYPEDEFS_FULL_TEXT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    topics: _containers.RepeatedScalarFieldContainer[str]
    types: _containers.RepeatedScalarFieldContainer[str]
    typedefs_full_text: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., topics: _Optional[_Iterable[str]] = ..., types: _Optional[_Iterable[str]] = ..., typedefs_full_text: _Optional[_Iterable[str]] = ...) -> None: ...
