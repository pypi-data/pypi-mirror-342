from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RosMsgType(_message.Message):
    __slots__ = ("md5", "name", "definition", "stamped")
    MD5_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DEFINITION_FIELD_NUMBER: _ClassVar[int]
    STAMPED_FIELD_NUMBER: _ClassVar[int]
    md5: str
    name: str
    definition: str
    stamped: bool
    def __init__(self, md5: _Optional[str] = ..., name: _Optional[str] = ..., definition: _Optional[str] = ..., stamped: bool = ...) -> None: ...
