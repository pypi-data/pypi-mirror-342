from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class JointTemperatures(_message.Message):
    __slots__ = ("temperatures",)
    TEMPERATURES_FIELD_NUMBER: _ClassVar[int]
    temperatures: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, temperatures: _Optional[_Iterable[float]] = ...) -> None: ...
