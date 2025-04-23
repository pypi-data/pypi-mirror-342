from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SmaccEventGenerator(_message.Message):
    __slots__ = ("index", "type_name", "object_tag")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
    OBJECT_TAG_FIELD_NUMBER: _ClassVar[int]
    index: int
    type_name: str
    object_tag: str
    def __init__(self, index: _Optional[int] = ..., type_name: _Optional[str] = ..., object_tag: _Optional[str] = ...) -> None: ...
