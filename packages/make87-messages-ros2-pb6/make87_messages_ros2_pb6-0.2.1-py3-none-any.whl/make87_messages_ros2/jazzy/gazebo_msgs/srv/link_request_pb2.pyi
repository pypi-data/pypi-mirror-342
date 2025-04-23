from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LinkRequestRequest(_message.Message):
    __slots__ = ("link_name",)
    LINK_NAME_FIELD_NUMBER: _ClassVar[int]
    link_name: str
    def __init__(self, link_name: _Optional[str] = ...) -> None: ...

class LinkRequestResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
