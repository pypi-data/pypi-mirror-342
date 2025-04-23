from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CommandLongRequest(_message.Message):
    __slots__ = ("broadcast", "command", "confirmation", "param1", "param2", "param3", "param4", "param5", "param6", "param7")
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
    def __init__(self, broadcast: bool = ..., command: _Optional[int] = ..., confirmation: _Optional[int] = ..., param1: _Optional[float] = ..., param2: _Optional[float] = ..., param3: _Optional[float] = ..., param4: _Optional[float] = ..., param5: _Optional[float] = ..., param6: _Optional[float] = ..., param7: _Optional[float] = ...) -> None: ...

class CommandLongResponse(_message.Message):
    __slots__ = ("success", "result")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    success: bool
    result: int
    def __init__(self, success: bool = ..., result: _Optional[int] = ...) -> None: ...
