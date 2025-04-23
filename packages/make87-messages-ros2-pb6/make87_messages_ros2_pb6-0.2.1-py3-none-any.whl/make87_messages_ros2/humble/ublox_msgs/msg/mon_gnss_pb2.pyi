from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MonGNSS(_message.Message):
    __slots__ = ("header", "version", "supported", "default_gnss", "enabled", "simultaneous", "reserved1")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    SUPPORTED_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_GNSS_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    SIMULTANEOUS_FIELD_NUMBER: _ClassVar[int]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    version: int
    supported: int
    default_gnss: int
    enabled: int
    simultaneous: int
    reserved1: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., version: _Optional[int] = ..., supported: _Optional[int] = ..., default_gnss: _Optional[int] = ..., enabled: _Optional[int] = ..., simultaneous: _Optional[int] = ..., reserved1: _Optional[_Iterable[int]] = ...) -> None: ...
