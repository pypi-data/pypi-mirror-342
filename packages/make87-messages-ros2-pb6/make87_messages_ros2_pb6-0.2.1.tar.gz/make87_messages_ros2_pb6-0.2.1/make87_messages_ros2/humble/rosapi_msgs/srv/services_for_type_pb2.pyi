from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ServicesForTypeRequest(_message.Message):
    __slots__ = ("header", "type")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    type: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., type: _Optional[str] = ...) -> None: ...

class ServicesForTypeResponse(_message.Message):
    __slots__ = ("header", "services")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SERVICES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    services: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., services: _Optional[_Iterable[str]] = ...) -> None: ...
