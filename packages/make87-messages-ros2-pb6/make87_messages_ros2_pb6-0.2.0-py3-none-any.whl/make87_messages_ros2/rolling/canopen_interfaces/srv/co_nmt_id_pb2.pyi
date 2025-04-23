from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CONmtIDRequest(_message.Message):
    __slots__ = ("nmtcommand", "nodeid")
    NMTCOMMAND_FIELD_NUMBER: _ClassVar[int]
    NODEID_FIELD_NUMBER: _ClassVar[int]
    nmtcommand: int
    nodeid: int
    def __init__(self, nmtcommand: _Optional[int] = ..., nodeid: _Optional[int] = ...) -> None: ...

class CONmtIDResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
