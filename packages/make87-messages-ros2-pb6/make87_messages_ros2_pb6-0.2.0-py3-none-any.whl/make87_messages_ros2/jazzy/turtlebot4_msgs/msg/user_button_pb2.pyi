from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class UserButton(_message.Message):
    __slots__ = ("button",)
    BUTTON_FIELD_NUMBER: _ClassVar[int]
    button: _containers.RepeatedScalarFieldContainer[bool]
    def __init__(self, button: _Optional[_Iterable[bool]] = ...) -> None: ...
