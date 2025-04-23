from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Inf(_message.Message):
    __slots__ = ("str",)
    STR_FIELD_NUMBER: _ClassVar[int]
    str: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, str: _Optional[_Iterable[int]] = ...) -> None: ...
