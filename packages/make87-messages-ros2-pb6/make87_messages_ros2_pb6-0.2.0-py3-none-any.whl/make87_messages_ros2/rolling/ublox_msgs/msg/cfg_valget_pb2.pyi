from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CfgVALGET(_message.Message):
    __slots__ = ("version", "layers", "position", "keys")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    version: int
    layers: int
    position: int
    keys: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, version: _Optional[int] = ..., layers: _Optional[int] = ..., position: _Optional[int] = ..., keys: _Optional[_Iterable[int]] = ...) -> None: ...
