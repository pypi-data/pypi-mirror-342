from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SmaccEvent(_message.Message):
    __slots__ = ("header", "event_type", "event_object_tag", "event_source", "label")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    EVENT_OBJECT_TAG_FIELD_NUMBER: _ClassVar[int]
    EVENT_SOURCE_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    event_type: str
    event_object_tag: str
    event_source: str
    label: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., event_type: _Optional[str] = ..., event_object_tag: _Optional[str] = ..., event_source: _Optional[str] = ..., label: _Optional[str] = ...) -> None: ...
