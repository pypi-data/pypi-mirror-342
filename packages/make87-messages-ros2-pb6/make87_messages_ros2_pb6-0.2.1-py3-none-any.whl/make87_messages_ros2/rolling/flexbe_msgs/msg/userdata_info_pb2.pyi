from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class UserdataInfo(_message.Message):
    __slots__ = ("state", "key", "type", "data")
    STATE_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    state: str
    key: str
    type: str
    data: str
    def __init__(self, state: _Optional[str] = ..., key: _Optional[str] = ..., type: _Optional[str] = ..., data: _Optional[str] = ...) -> None: ...
