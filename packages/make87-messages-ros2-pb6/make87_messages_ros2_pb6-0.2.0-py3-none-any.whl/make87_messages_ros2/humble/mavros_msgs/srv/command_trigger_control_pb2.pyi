from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CommandTriggerControlRequest(_message.Message):
    __slots__ = ("header", "trigger_enable", "sequence_reset", "trigger_pause")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_ENABLE_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_RESET_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_PAUSE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    trigger_enable: bool
    sequence_reset: bool
    trigger_pause: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., trigger_enable: bool = ..., sequence_reset: bool = ..., trigger_pause: bool = ...) -> None: ...

class CommandTriggerControlResponse(_message.Message):
    __slots__ = ("header", "success", "result")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    result: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., result: _Optional[int] = ...) -> None: ...
