from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AddDiagnosticsRequest(_message.Message):
    __slots__ = ("load_namespace",)
    LOAD_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    load_namespace: str
    def __init__(self, load_namespace: _Optional[str] = ...) -> None: ...

class AddDiagnosticsResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...
