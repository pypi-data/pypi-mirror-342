from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetCommandRequest(_message.Message):
    __slots__ = ("header", "max_repeats", "set_commands", "position_command")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MAX_REPEATS_FIELD_NUMBER: _ClassVar[int]
    SET_COMMANDS_FIELD_NUMBER: _ClassVar[int]
    POSITION_COMMAND_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    max_repeats: int
    set_commands: bool
    position_command: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., max_repeats: _Optional[int] = ..., set_commands: bool = ..., position_command: _Optional[int] = ...) -> None: ...

class SetCommandResponse(_message.Message):
    __slots__ = ("header", "success")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ...) -> None: ...
