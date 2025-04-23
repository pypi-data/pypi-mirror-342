from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class MicroROSDiagnosticKeyValue(_message.Message):
    __slots__ = ("level", "key", "value_type", "bool_value", "int_value", "double_value", "value_id")
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_TYPE_FIELD_NUMBER: _ClassVar[int]
    BOOL_VALUE_FIELD_NUMBER: _ClassVar[int]
    INT_VALUE_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_VALUE_FIELD_NUMBER: _ClassVar[int]
    VALUE_ID_FIELD_NUMBER: _ClassVar[int]
    level: int
    key: int
    value_type: int
    bool_value: bool
    int_value: int
    double_value: float
    value_id: int
    def __init__(self, level: _Optional[int] = ..., key: _Optional[int] = ..., value_type: _Optional[int] = ..., bool_value: bool = ..., int_value: _Optional[int] = ..., double_value: _Optional[float] = ..., value_id: _Optional[int] = ...) -> None: ...
