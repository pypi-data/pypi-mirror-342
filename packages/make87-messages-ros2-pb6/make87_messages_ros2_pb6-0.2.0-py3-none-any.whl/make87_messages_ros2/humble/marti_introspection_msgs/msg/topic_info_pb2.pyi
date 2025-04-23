from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TopicInfo(_message.Message):
    __slots__ = ("header", "name", "resolved_name", "description", "group", "message_type", "advertised")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    RESOLVED_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ADVERTISED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    resolved_name: str
    description: str
    group: str
    message_type: str
    advertised: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., resolved_name: _Optional[str] = ..., description: _Optional[str] = ..., group: _Optional[str] = ..., message_type: _Optional[str] = ..., advertised: bool = ...) -> None: ...
