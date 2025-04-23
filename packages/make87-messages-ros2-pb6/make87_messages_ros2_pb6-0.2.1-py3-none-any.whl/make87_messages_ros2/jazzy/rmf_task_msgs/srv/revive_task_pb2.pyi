from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ReviveTaskRequest(_message.Message):
    __slots__ = ("requester", "task_id")
    REQUESTER_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    requester: str
    task_id: str
    def __init__(self, requester: _Optional[str] = ..., task_id: _Optional[str] = ...) -> None: ...

class ReviveTaskResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
