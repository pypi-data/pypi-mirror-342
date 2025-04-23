from make87_messages_ros2.rolling.rmf_task_msgs.msg import assignment_pb2 as _assignment_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DispatchState(_message.Message):
    __slots__ = ("task_id", "status", "assignment", "errors")
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNMENT_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    status: int
    assignment: _assignment_pb2.Assignment
    errors: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, task_id: _Optional[str] = ..., status: _Optional[int] = ..., assignment: _Optional[_Union[_assignment_pb2.Assignment, _Mapping]] = ..., errors: _Optional[_Iterable[str]] = ...) -> None: ...
