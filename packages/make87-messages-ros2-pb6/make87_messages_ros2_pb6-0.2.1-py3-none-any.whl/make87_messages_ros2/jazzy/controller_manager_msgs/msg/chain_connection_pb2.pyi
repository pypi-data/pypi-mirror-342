from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ChainConnection(_message.Message):
    __slots__ = ("name", "reference_interfaces")
    NAME_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_INTERFACES_FIELD_NUMBER: _ClassVar[int]
    name: str
    reference_interfaces: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., reference_interfaces: _Optional[_Iterable[str]] = ...) -> None: ...
