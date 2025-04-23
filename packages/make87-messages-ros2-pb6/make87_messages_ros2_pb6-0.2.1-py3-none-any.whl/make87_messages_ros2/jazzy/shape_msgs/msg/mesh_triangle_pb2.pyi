from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class MeshTriangle(_message.Message):
    __slots__ = ("vertex_indices",)
    VERTEX_INDICES_FIELD_NUMBER: _ClassVar[int]
    vertex_indices: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, vertex_indices: _Optional[_Iterable[int]] = ...) -> None: ...
