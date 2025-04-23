from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ActionExecution(_message.Message):
    __slots__ = ("type", "node_id", "action", "arguments", "success", "completion", "status")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    type: int
    node_id: str
    action: str
    arguments: _containers.RepeatedScalarFieldContainer[str]
    success: bool
    completion: float
    status: str
    def __init__(self, type: _Optional[int] = ..., node_id: _Optional[str] = ..., action: _Optional[str] = ..., arguments: _Optional[_Iterable[str]] = ..., success: bool = ..., completion: _Optional[float] = ..., status: _Optional[str] = ...) -> None: ...
