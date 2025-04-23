from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class MonGNSS(_message.Message):
    __slots__ = ("version", "supported", "default_gnss", "enabled", "simultaneous", "reserved1")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    SUPPORTED_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_GNSS_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    SIMULTANEOUS_FIELD_NUMBER: _ClassVar[int]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    version: int
    supported: int
    default_gnss: int
    enabled: int
    simultaneous: int
    reserved1: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, version: _Optional[int] = ..., supported: _Optional[int] = ..., default_gnss: _Optional[int] = ..., enabled: _Optional[int] = ..., simultaneous: _Optional[int] = ..., reserved1: _Optional[_Iterable[int]] = ...) -> None: ...
