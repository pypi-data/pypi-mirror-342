from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class IsProgramSavedRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class IsProgramSavedResponse(_message.Message):
    __slots__ = ("answer", "program_name", "program_saved", "success")
    ANSWER_FIELD_NUMBER: _ClassVar[int]
    PROGRAM_NAME_FIELD_NUMBER: _ClassVar[int]
    PROGRAM_SAVED_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    answer: str
    program_name: str
    program_saved: bool
    success: bool
    def __init__(self, answer: _Optional[str] = ..., program_name: _Optional[str] = ..., program_saved: bool = ..., success: bool = ...) -> None: ...
