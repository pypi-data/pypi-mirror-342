from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class UnregisterParticipantRequest(_message.Message):
    __slots__ = ("participant_id",)
    PARTICIPANT_ID_FIELD_NUMBER: _ClassVar[int]
    participant_id: int
    def __init__(self, participant_id: _Optional[int] = ...) -> None: ...

class UnregisterParticipantResponse(_message.Message):
    __slots__ = ("confirmation", "error")
    CONFIRMATION_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    confirmation: bool
    error: str
    def __init__(self, confirmation: bool = ..., error: _Optional[str] = ...) -> None: ...
