from make87_messages_ros2.jazzy.rmf_task_msgs.msg import dispatch_state_pb2 as _dispatch_state_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DispatchStates(_message.Message):
    __slots__ = ("active", "finished")
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    FINISHED_FIELD_NUMBER: _ClassVar[int]
    active: _containers.RepeatedCompositeFieldContainer[_dispatch_state_pb2.DispatchState]
    finished: _containers.RepeatedCompositeFieldContainer[_dispatch_state_pb2.DispatchState]
    def __init__(self, active: _Optional[_Iterable[_Union[_dispatch_state_pb2.DispatchState, _Mapping]]] = ..., finished: _Optional[_Iterable[_Union[_dispatch_state_pb2.DispatchState, _Mapping]]] = ...) -> None: ...
