from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CommandLongRequest(_message.Message):
    __slots__ = ("header", "broadcast", "command", "confirmation", "param1", "param2", "param3", "param4", "param5", "param6", "param7")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BROADCAST_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    CONFIRMATION_FIELD_NUMBER: _ClassVar[int]
    PARAM1_FIELD_NUMBER: _ClassVar[int]
    PARAM2_FIELD_NUMBER: _ClassVar[int]
    PARAM3_FIELD_NUMBER: _ClassVar[int]
    PARAM4_FIELD_NUMBER: _ClassVar[int]
    PARAM5_FIELD_NUMBER: _ClassVar[int]
    PARAM6_FIELD_NUMBER: _ClassVar[int]
    PARAM7_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    broadcast: bool
    command: int
    confirmation: int
    param1: float
    param2: float
    param3: float
    param4: float
    param5: float
    param6: float
    param7: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., broadcast: bool = ..., command: _Optional[int] = ..., confirmation: _Optional[int] = ..., param1: _Optional[float] = ..., param2: _Optional[float] = ..., param3: _Optional[float] = ..., param4: _Optional[float] = ..., param5: _Optional[float] = ..., param6: _Optional[float] = ..., param7: _Optional[float] = ...) -> None: ...

class CommandLongResponse(_message.Message):
    __slots__ = ("header", "success", "result")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    result: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., result: _Optional[int] = ...) -> None: ...
