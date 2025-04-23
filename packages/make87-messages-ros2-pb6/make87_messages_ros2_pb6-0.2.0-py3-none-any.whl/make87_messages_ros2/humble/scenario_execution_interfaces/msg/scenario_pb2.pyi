from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Scenario(_message.Message):
    __slots__ = ("header", "name", "scenario_file")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SCENARIO_FILE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    scenario_file: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., scenario_file: _Optional[str] = ...) -> None: ...
