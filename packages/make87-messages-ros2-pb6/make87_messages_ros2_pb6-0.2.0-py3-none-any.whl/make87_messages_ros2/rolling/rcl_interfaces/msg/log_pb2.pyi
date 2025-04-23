from make87_messages_ros2.rolling.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Log(_message.Message):
    __slots__ = ("stamp", "level", "name", "msg", "file", "function", "line")
    STAMP_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    LINE_FIELD_NUMBER: _ClassVar[int]
    stamp: _time_pb2.Time
    level: int
    name: str
    msg: str
    file: str
    function: str
    line: int
    def __init__(self, stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., level: _Optional[int] = ..., name: _Optional[str] = ..., msg: _Optional[str] = ..., file: _Optional[str] = ..., function: _Optional[str] = ..., line: _Optional[int] = ...) -> None: ...
