from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ReadSplitEvent(_message.Message):
    __slots__ = ("header", "closed_file", "opened_file")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CLOSED_FILE_FIELD_NUMBER: _ClassVar[int]
    OPENED_FILE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    closed_file: str
    opened_file: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., closed_file: _Optional[str] = ..., opened_file: _Optional[str] = ...) -> None: ...
