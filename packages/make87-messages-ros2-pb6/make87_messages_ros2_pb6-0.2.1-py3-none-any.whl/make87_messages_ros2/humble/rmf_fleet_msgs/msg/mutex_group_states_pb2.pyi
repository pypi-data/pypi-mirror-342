from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_fleet_msgs.msg import mutex_group_assignment_pb2 as _mutex_group_assignment_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MutexGroupStates(_message.Message):
    __slots__ = ("header", "assignments")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ASSIGNMENTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    assignments: _containers.RepeatedCompositeFieldContainer[_mutex_group_assignment_pb2.MutexGroupAssignment]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., assignments: _Optional[_Iterable[_Union[_mutex_group_assignment_pb2.MutexGroupAssignment, _Mapping]]] = ...) -> None: ...
