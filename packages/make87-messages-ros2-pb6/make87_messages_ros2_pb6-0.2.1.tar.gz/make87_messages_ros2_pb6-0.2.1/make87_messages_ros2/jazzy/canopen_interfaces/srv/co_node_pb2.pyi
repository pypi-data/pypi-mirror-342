from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CONodeRequest(_message.Message):
    __slots__ = ("nodeid",)
    NODEID_FIELD_NUMBER: _ClassVar[int]
    nodeid: int
    def __init__(self, nodeid: _Optional[int] = ...) -> None: ...

class CONodeResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
