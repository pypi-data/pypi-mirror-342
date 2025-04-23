from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SmaccEventGenerator(_message.Message):
    __slots__ = ("header", "index", "type_name", "object_tag")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
    OBJECT_TAG_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    index: int
    type_name: str
    object_tag: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., index: _Optional[int] = ..., type_name: _Optional[str] = ..., object_tag: _Optional[str] = ...) -> None: ...
