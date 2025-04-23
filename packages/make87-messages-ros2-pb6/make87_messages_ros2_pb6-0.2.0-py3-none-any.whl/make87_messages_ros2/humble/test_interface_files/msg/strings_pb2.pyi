from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Strings(_message.Message):
    __slots__ = ("header", "string_value", "string_value_default1", "string_value_default2", "string_value_default3", "string_value_default4", "string_value_default5", "bounded_string_value", "bounded_string_value_default1", "bounded_string_value_default2", "bounded_string_value_default3", "bounded_string_value_default4", "bounded_string_value_default5")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
    STRING_VALUE_DEFAULT1_FIELD_NUMBER: _ClassVar[int]
    STRING_VALUE_DEFAULT2_FIELD_NUMBER: _ClassVar[int]
    STRING_VALUE_DEFAULT3_FIELD_NUMBER: _ClassVar[int]
    STRING_VALUE_DEFAULT4_FIELD_NUMBER: _ClassVar[int]
    STRING_VALUE_DEFAULT5_FIELD_NUMBER: _ClassVar[int]
    BOUNDED_STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
    BOUNDED_STRING_VALUE_DEFAULT1_FIELD_NUMBER: _ClassVar[int]
    BOUNDED_STRING_VALUE_DEFAULT2_FIELD_NUMBER: _ClassVar[int]
    BOUNDED_STRING_VALUE_DEFAULT3_FIELD_NUMBER: _ClassVar[int]
    BOUNDED_STRING_VALUE_DEFAULT4_FIELD_NUMBER: _ClassVar[int]
    BOUNDED_STRING_VALUE_DEFAULT5_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    string_value: str
    string_value_default1: str
    string_value_default2: str
    string_value_default3: str
    string_value_default4: str
    string_value_default5: str
    bounded_string_value: str
    bounded_string_value_default1: str
    bounded_string_value_default2: str
    bounded_string_value_default3: str
    bounded_string_value_default4: str
    bounded_string_value_default5: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., string_value: _Optional[str] = ..., string_value_default1: _Optional[str] = ..., string_value_default2: _Optional[str] = ..., string_value_default3: _Optional[str] = ..., string_value_default4: _Optional[str] = ..., string_value_default5: _Optional[str] = ..., bounded_string_value: _Optional[str] = ..., bounded_string_value_default1: _Optional[str] = ..., bounded_string_value_default2: _Optional[str] = ..., bounded_string_value_default3: _Optional[str] = ..., bounded_string_value_default4: _Optional[str] = ..., bounded_string_value_default5: _Optional[str] = ...) -> None: ...
