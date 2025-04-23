from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetAvailableModesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetAvailableModesResponse(_message.Message):
    __slots__ = ("available_modes",)
    AVAILABLE_MODES_FIELD_NUMBER: _ClassVar[int]
    available_modes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, available_modes: _Optional[_Iterable[str]] = ...) -> None: ...
