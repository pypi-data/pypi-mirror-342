from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Edges(_message.Message):
    __slots__ = ("node_ids", "weights")
    NODE_IDS_FIELD_NUMBER: _ClassVar[int]
    WEIGHTS_FIELD_NUMBER: _ClassVar[int]
    node_ids: _containers.RepeatedScalarFieldContainer[int]
    weights: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, node_ids: _Optional[_Iterable[int]] = ..., weights: _Optional[_Iterable[float]] = ...) -> None: ...
