from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BasicTypes(_message.Message):
    __slots__ = ("bool_value", "byte_value", "char_value", "float32_value", "float64_value", "int8_value", "uint8_value", "int16_value", "uint16_value", "int32_value", "uint32_value", "int64_value", "uint64_value")
    BOOL_VALUE_FIELD_NUMBER: _ClassVar[int]
    BYTE_VALUE_FIELD_NUMBER: _ClassVar[int]
    CHAR_VALUE_FIELD_NUMBER: _ClassVar[int]
    FLOAT32_VALUE_FIELD_NUMBER: _ClassVar[int]
    FLOAT64_VALUE_FIELD_NUMBER: _ClassVar[int]
    INT8_VALUE_FIELD_NUMBER: _ClassVar[int]
    UINT8_VALUE_FIELD_NUMBER: _ClassVar[int]
    INT16_VALUE_FIELD_NUMBER: _ClassVar[int]
    UINT16_VALUE_FIELD_NUMBER: _ClassVar[int]
    INT32_VALUE_FIELD_NUMBER: _ClassVar[int]
    UINT32_VALUE_FIELD_NUMBER: _ClassVar[int]
    INT64_VALUE_FIELD_NUMBER: _ClassVar[int]
    UINT64_VALUE_FIELD_NUMBER: _ClassVar[int]
    bool_value: bool
    byte_value: int
    char_value: int
    float32_value: float
    float64_value: float
    int8_value: int
    uint8_value: int
    int16_value: int
    uint16_value: int
    int32_value: int
    uint32_value: int
    int64_value: int
    uint64_value: int
    def __init__(self, bool_value: bool = ..., byte_value: _Optional[int] = ..., char_value: _Optional[int] = ..., float32_value: _Optional[float] = ..., float64_value: _Optional[float] = ..., int8_value: _Optional[int] = ..., uint8_value: _Optional[int] = ..., int16_value: _Optional[int] = ..., uint16_value: _Optional[int] = ..., int32_value: _Optional[int] = ..., uint32_value: _Optional[int] = ..., int64_value: _Optional[int] = ..., uint64_value: _Optional[int] = ...) -> None: ...
