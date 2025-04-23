from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SmaccOrthogonal(_message.Message):
    __slots__ = ("name", "client_behavior_names", "client_names")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CLIENT_BEHAVIOR_NAMES_FIELD_NUMBER: _ClassVar[int]
    CLIENT_NAMES_FIELD_NUMBER: _ClassVar[int]
    name: str
    client_behavior_names: _containers.RepeatedScalarFieldContainer[str]
    client_names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., client_behavior_names: _Optional[_Iterable[str]] = ..., client_names: _Optional[_Iterable[str]] = ...) -> None: ...
