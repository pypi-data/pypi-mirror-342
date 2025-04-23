from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class WriteSplitEvent(_message.Message):
    __slots__ = ("closed_file", "opened_file", "node_name")
    CLOSED_FILE_FIELD_NUMBER: _ClassVar[int]
    OPENED_FILE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    closed_file: str
    opened_file: str
    node_name: str
    def __init__(self, closed_file: _Optional[str] = ..., opened_file: _Optional[str] = ..., node_name: _Optional[str] = ...) -> None: ...
