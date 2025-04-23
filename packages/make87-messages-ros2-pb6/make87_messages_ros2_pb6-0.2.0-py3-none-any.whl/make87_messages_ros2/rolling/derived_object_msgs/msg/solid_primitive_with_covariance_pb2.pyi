from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SolidPrimitiveWithCovariance(_message.Message):
    __slots__ = ("type", "dimensions", "covariance")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    type: int
    dimensions: _containers.RepeatedScalarFieldContainer[float]
    covariance: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, type: _Optional[int] = ..., dimensions: _Optional[_Iterable[float]] = ..., covariance: _Optional[_Iterable[float]] = ...) -> None: ...
