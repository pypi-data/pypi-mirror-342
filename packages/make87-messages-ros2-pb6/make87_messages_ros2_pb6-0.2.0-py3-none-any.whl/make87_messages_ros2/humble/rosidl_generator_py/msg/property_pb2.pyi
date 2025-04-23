from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Property(_message.Message):
    __slots__ = ("header", "property", "anything")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PROPERTY_FIELD_NUMBER: _ClassVar[int]
    ANYTHING_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    property: str
    anything: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., property: _Optional[str] = ..., anything: _Optional[str] = ...) -> None: ...
