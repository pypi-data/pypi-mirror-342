from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetBlackboardVariablesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBlackboardVariablesResponse(_message.Message):
    __slots__ = ("variables",)
    VARIABLES_FIELD_NUMBER: _ClassVar[int]
    variables: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, variables: _Optional[_Iterable[str]] = ...) -> None: ...
