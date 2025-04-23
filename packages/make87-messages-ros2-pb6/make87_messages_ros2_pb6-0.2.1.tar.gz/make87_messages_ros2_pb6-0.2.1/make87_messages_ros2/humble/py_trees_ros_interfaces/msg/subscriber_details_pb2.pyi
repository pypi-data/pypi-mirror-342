from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SubscriberDetails(_message.Message):
    __slots__ = ("header", "topic_name", "message_type", "latched")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TOPIC_NAME_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    LATCHED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    topic_name: str
    message_type: str
    latched: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., topic_name: _Optional[str] = ..., message_type: _Optional[str] = ..., latched: bool = ...) -> None: ...
