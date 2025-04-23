from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Loop(_message.Message):
    __slots__ = ("header", "task_id", "robot_type", "num_loops", "start_name", "finish_name")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    ROBOT_TYPE_FIELD_NUMBER: _ClassVar[int]
    NUM_LOOPS_FIELD_NUMBER: _ClassVar[int]
    START_NAME_FIELD_NUMBER: _ClassVar[int]
    FINISH_NAME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    task_id: str
    robot_type: str
    num_loops: int
    start_name: str
    finish_name: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., task_id: _Optional[str] = ..., robot_type: _Optional[str] = ..., num_loops: _Optional[int] = ..., start_name: _Optional[str] = ..., finish_name: _Optional[str] = ...) -> None: ...
