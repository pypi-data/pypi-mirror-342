from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ActionPerformerStatus(_message.Message):
    __slots__ = ("status_stamp", "state", "action", "specialized_arguments", "node_name")
    STATUS_STAMP_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    SPECIALIZED_ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    status_stamp: _time_pb2.Time
    state: int
    action: str
    specialized_arguments: _containers.RepeatedScalarFieldContainer[str]
    node_name: str
    def __init__(self, status_stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., state: _Optional[int] = ..., action: _Optional[str] = ..., specialized_arguments: _Optional[_Iterable[str]] = ..., node_name: _Optional[str] = ...) -> None: ...
