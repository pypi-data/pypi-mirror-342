from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class FieldSetReadSrvRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FieldSetReadSrvResponse(_message.Message):
    __slots__ = ("field_set_selection_method", "active_field_set", "success")
    FIELD_SET_SELECTION_METHOD_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_SET_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    field_set_selection_method: int
    active_field_set: int
    success: bool
    def __init__(self, field_set_selection_method: _Optional[int] = ..., active_field_set: _Optional[int] = ..., success: bool = ...) -> None: ...
