from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PlannerParams(_message.Message):
    __slots__ = ("keys", "values", "descriptions")
    KEYS_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTIONS_FIELD_NUMBER: _ClassVar[int]
    keys: _containers.RepeatedScalarFieldContainer[str]
    values: _containers.RepeatedScalarFieldContainer[str]
    descriptions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, keys: _Optional[_Iterable[str]] = ..., values: _Optional[_Iterable[str]] = ..., descriptions: _Optional[_Iterable[str]] = ...) -> None: ...
