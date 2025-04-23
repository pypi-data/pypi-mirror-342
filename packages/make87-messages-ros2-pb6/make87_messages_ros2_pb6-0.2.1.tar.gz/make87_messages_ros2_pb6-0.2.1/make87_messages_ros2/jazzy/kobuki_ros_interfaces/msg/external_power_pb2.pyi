from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ExternalPower(_message.Message):
    __slots__ = ("source", "state")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    source: int
    state: int
    def __init__(self, source: _Optional[int] = ..., state: _Optional[int] = ...) -> None: ...
