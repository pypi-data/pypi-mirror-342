from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PublisherDetails(_message.Message):
    __slots__ = ("topic_name", "message_type", "latched")
    TOPIC_NAME_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    LATCHED_FIELD_NUMBER: _ClassVar[int]
    topic_name: str
    message_type: str
    latched: bool
    def __init__(self, topic_name: _Optional[str] = ..., message_type: _Optional[str] = ..., latched: bool = ...) -> None: ...
