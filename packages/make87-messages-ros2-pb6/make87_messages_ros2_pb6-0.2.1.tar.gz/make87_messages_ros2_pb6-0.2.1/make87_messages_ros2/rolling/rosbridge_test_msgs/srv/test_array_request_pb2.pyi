from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class TestArrayRequestRequest(_message.Message):
    __slots__ = ("int_values",)
    INT_VALUES_FIELD_NUMBER: _ClassVar[int]
    int_values: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, int_values: _Optional[_Iterable[int]] = ...) -> None: ...

class TestArrayRequestResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
