from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CommandTriggerIntervalRequest(_message.Message):
    __slots__ = ("header", "cycle_time", "integration_time")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CYCLE_TIME_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_TIME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    cycle_time: float
    integration_time: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., cycle_time: _Optional[float] = ..., integration_time: _Optional[float] = ...) -> None: ...

class CommandTriggerIntervalResponse(_message.Message):
    __slots__ = ("header", "success", "result")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    result: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., result: _Optional[int] = ...) -> None: ...
