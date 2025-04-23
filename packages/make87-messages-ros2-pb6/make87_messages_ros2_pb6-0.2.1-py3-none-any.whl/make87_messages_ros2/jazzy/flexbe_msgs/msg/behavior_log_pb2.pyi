from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BehaviorLog(_message.Message):
    __slots__ = ("text", "status_code")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    text: str
    status_code: int
    def __init__(self, text: _Optional[str] = ..., status_code: _Optional[int] = ...) -> None: ...
