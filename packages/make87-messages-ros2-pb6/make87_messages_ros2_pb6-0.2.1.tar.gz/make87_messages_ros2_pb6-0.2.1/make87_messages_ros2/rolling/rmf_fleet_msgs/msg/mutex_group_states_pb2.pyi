from make87_messages_ros2.rolling.rmf_fleet_msgs.msg import mutex_group_assignment_pb2 as _mutex_group_assignment_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MutexGroupStates(_message.Message):
    __slots__ = ("assignments",)
    ASSIGNMENTS_FIELD_NUMBER: _ClassVar[int]
    assignments: _containers.RepeatedCompositeFieldContainer[_mutex_group_assignment_pb2.MutexGroupAssignment]
    def __init__(self, assignments: _Optional[_Iterable[_Union[_mutex_group_assignment_pb2.MutexGroupAssignment, _Mapping]]] = ...) -> None: ...
