from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StringArrays(_message.Message):
    __slots__ = ("header", "ub_string_static_array_value", "ub_string_ub_array_value", "ub_string_dynamic_array_value", "string_dynamic_array_value", "string_static_array_value", "string_bounded_array_value", "def_string_dynamic_array_value", "def_string_static_array_value", "def_string_bounded_array_value", "def_various_quotes", "def_various_commas")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    UB_STRING_STATIC_ARRAY_VALUE_FIELD_NUMBER: _ClassVar[int]
    UB_STRING_UB_ARRAY_VALUE_FIELD_NUMBER: _ClassVar[int]
    UB_STRING_DYNAMIC_ARRAY_VALUE_FIELD_NUMBER: _ClassVar[int]
    STRING_DYNAMIC_ARRAY_VALUE_FIELD_NUMBER: _ClassVar[int]
    STRING_STATIC_ARRAY_VALUE_FIELD_NUMBER: _ClassVar[int]
    STRING_BOUNDED_ARRAY_VALUE_FIELD_NUMBER: _ClassVar[int]
    DEF_STRING_DYNAMIC_ARRAY_VALUE_FIELD_NUMBER: _ClassVar[int]
    DEF_STRING_STATIC_ARRAY_VALUE_FIELD_NUMBER: _ClassVar[int]
    DEF_STRING_BOUNDED_ARRAY_VALUE_FIELD_NUMBER: _ClassVar[int]
    DEF_VARIOUS_QUOTES_FIELD_NUMBER: _ClassVar[int]
    DEF_VARIOUS_COMMAS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ub_string_static_array_value: _containers.RepeatedScalarFieldContainer[str]
    ub_string_ub_array_value: _containers.RepeatedScalarFieldContainer[str]
    ub_string_dynamic_array_value: _containers.RepeatedScalarFieldContainer[str]
    string_dynamic_array_value: _containers.RepeatedScalarFieldContainer[str]
    string_static_array_value: _containers.RepeatedScalarFieldContainer[str]
    string_bounded_array_value: _containers.RepeatedScalarFieldContainer[str]
    def_string_dynamic_array_value: _containers.RepeatedScalarFieldContainer[str]
    def_string_static_array_value: _containers.RepeatedScalarFieldContainer[str]
    def_string_bounded_array_value: _containers.RepeatedScalarFieldContainer[str]
    def_various_quotes: _containers.RepeatedScalarFieldContainer[str]
    def_various_commas: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ub_string_static_array_value: _Optional[_Iterable[str]] = ..., ub_string_ub_array_value: _Optional[_Iterable[str]] = ..., ub_string_dynamic_array_value: _Optional[_Iterable[str]] = ..., string_dynamic_array_value: _Optional[_Iterable[str]] = ..., string_static_array_value: _Optional[_Iterable[str]] = ..., string_bounded_array_value: _Optional[_Iterable[str]] = ..., def_string_dynamic_array_value: _Optional[_Iterable[str]] = ..., def_string_static_array_value: _Optional[_Iterable[str]] = ..., def_string_bounded_array_value: _Optional[_Iterable[str]] = ..., def_various_quotes: _Optional[_Iterable[str]] = ..., def_various_commas: _Optional[_Iterable[str]] = ...) -> None: ...
