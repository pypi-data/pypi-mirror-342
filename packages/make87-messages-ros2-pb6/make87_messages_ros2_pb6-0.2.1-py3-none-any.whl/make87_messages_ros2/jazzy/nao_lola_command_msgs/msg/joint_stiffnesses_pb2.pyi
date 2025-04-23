from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class JointStiffnesses(_message.Message):
    __slots__ = ("indexes", "stiffnesses")
    INDEXES_FIELD_NUMBER: _ClassVar[int]
    STIFFNESSES_FIELD_NUMBER: _ClassVar[int]
    indexes: _containers.RepeatedScalarFieldContainer[int]
    stiffnesses: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, indexes: _Optional[_Iterable[int]] = ..., stiffnesses: _Optional[_Iterable[float]] = ...) -> None: ...
