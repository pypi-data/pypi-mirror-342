from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TmcCustomCmdRequest(_message.Message):
    __slots__ = ("header", "instruction", "instruction_type", "motor_num", "value")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    INSTRUCTION_FIELD_NUMBER: _ClassVar[int]
    INSTRUCTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    MOTOR_NUM_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    instruction: str
    instruction_type: int
    motor_num: int
    value: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., instruction: _Optional[str] = ..., instruction_type: _Optional[int] = ..., motor_num: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...

class TmcCustomCmdResponse(_message.Message):
    __slots__ = ("header", "output", "result")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    output: int
    result: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., output: _Optional[int] = ..., result: bool = ...) -> None: ...
