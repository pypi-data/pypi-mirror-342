from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Transition(_message.Message):
    __slots__ = ("outcome", "state")
    OUTCOME_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    outcome: str
    state: str
    def __init__(self, outcome: _Optional[str] = ..., state: _Optional[str] = ...) -> None: ...
