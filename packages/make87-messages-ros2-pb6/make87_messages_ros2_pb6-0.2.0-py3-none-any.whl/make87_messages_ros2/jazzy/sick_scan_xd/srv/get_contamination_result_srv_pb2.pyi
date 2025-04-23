from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetContaminationResultSrvRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetContaminationResultSrvResponse(_message.Message):
    __slots__ = ("warning", "error", "success")
    WARNING_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    warning: int
    error: int
    success: bool
    def __init__(self, warning: _Optional[int] = ..., error: _Optional[int] = ..., success: bool = ...) -> None: ...
