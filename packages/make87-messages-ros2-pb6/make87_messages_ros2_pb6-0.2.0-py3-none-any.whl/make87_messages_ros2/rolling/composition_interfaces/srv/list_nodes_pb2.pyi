from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ListNodesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListNodesResponse(_message.Message):
    __slots__ = ("full_node_names", "unique_ids")
    FULL_NODE_NAMES_FIELD_NUMBER: _ClassVar[int]
    UNIQUE_IDS_FIELD_NUMBER: _ClassVar[int]
    full_node_names: _containers.RepeatedScalarFieldContainer[str]
    unique_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, full_node_names: _Optional[_Iterable[str]] = ..., unique_ids: _Optional[_Iterable[int]] = ...) -> None: ...
