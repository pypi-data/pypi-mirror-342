from make87_messages_ros2.jazzy.std_msgs.msg import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetProblemRequest(_message.Message):
    __slots__ = ("request",)
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    request: _empty_pb2.Empty
    def __init__(self, request: _Optional[_Union[_empty_pb2.Empty, _Mapping]] = ...) -> None: ...

class GetProblemResponse(_message.Message):
    __slots__ = ("success", "problem", "error_info")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    PROBLEM_FIELD_NUMBER: _ClassVar[int]
    ERROR_INFO_FIELD_NUMBER: _ClassVar[int]
    success: bool
    problem: str
    error_info: str
    def __init__(self, success: bool = ..., problem: _Optional[str] = ..., error_info: _Optional[str] = ...) -> None: ...
