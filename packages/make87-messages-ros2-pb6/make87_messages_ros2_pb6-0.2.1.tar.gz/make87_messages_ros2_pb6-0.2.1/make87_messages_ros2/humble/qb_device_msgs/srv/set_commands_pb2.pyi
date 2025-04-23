from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetCommandsRequest(_message.Message):
    __slots__ = ("header", "id", "max_repeats", "set_commands", "set_commands_async", "commands")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    MAX_REPEATS_FIELD_NUMBER: _ClassVar[int]
    SET_COMMANDS_FIELD_NUMBER: _ClassVar[int]
    SET_COMMANDS_ASYNC_FIELD_NUMBER: _ClassVar[int]
    COMMANDS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    id: int
    max_repeats: int
    set_commands: bool
    set_commands_async: bool
    commands: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., id: _Optional[int] = ..., max_repeats: _Optional[int] = ..., set_commands: bool = ..., set_commands_async: bool = ..., commands: _Optional[_Iterable[int]] = ...) -> None: ...

class SetCommandsResponse(_message.Message):
    __slots__ = ("header", "success", "failures")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    FAILURES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    failures: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., failures: _Optional[int] = ...) -> None: ...
