from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ParameterValue(_message.Message):
    __slots__ = ("type", "bool_value", "integer_value", "double_value", "string_value", "byte_array_value", "bool_array_value", "integer_array_value", "double_array_value", "string_array_value")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    BOOL_VALUE_FIELD_NUMBER: _ClassVar[int]
    INTEGER_VALUE_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_VALUE_FIELD_NUMBER: _ClassVar[int]
    STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
    BYTE_ARRAY_VALUE_FIELD_NUMBER: _ClassVar[int]
    BOOL_ARRAY_VALUE_FIELD_NUMBER: _ClassVar[int]
    INTEGER_ARRAY_VALUE_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_ARRAY_VALUE_FIELD_NUMBER: _ClassVar[int]
    STRING_ARRAY_VALUE_FIELD_NUMBER: _ClassVar[int]
    type: int
    bool_value: bool
    integer_value: int
    double_value: float
    string_value: str
    byte_array_value: _containers.RepeatedScalarFieldContainer[int]
    bool_array_value: _containers.RepeatedScalarFieldContainer[bool]
    integer_array_value: _containers.RepeatedScalarFieldContainer[int]
    double_array_value: _containers.RepeatedScalarFieldContainer[float]
    string_array_value: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, type: _Optional[int] = ..., bool_value: bool = ..., integer_value: _Optional[int] = ..., double_value: _Optional[float] = ..., string_value: _Optional[str] = ..., byte_array_value: _Optional[_Iterable[int]] = ..., bool_array_value: _Optional[_Iterable[bool]] = ..., integer_array_value: _Optional[_Iterable[int]] = ..., double_array_value: _Optional[_Iterable[float]] = ..., string_array_value: _Optional[_Iterable[str]] = ...) -> None: ...
