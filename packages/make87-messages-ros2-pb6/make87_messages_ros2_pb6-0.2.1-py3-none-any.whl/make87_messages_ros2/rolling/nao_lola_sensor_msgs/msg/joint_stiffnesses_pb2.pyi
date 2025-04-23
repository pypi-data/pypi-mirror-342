from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class JointStiffnesses(_message.Message):
    __slots__ = ("stiffnesses",)
    STIFFNESSES_FIELD_NUMBER: _ClassVar[int]
    stiffnesses: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, stiffnesses: _Optional[_Iterable[float]] = ...) -> None: ...
