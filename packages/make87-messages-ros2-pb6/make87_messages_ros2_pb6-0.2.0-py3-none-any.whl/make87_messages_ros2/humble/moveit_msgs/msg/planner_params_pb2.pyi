from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PlannerParams(_message.Message):
    __slots__ = ("header", "keys", "values", "descriptions")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTIONS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    keys: _containers.RepeatedScalarFieldContainer[str]
    values: _containers.RepeatedScalarFieldContainer[str]
    descriptions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., keys: _Optional[_Iterable[str]] = ..., values: _Optional[_Iterable[str]] = ..., descriptions: _Optional[_Iterable[str]] = ...) -> None: ...
