from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class NegotiationRefusal(_message.Message):
    __slots__ = ("conflict_version",)
    CONFLICT_VERSION_FIELD_NUMBER: _ClassVar[int]
    conflict_version: int
    def __init__(self, conflict_version: _Optional[int] = ...) -> None: ...
