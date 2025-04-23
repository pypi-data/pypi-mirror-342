from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Param(_message.Message):
    __slots__ = ("name", "type", "sub_types")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SUB_TYPES_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: str
    sub_types: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., type: _Optional[str] = ..., sub_types: _Optional[_Iterable[str]] = ...) -> None: ...
