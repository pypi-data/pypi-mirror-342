from make87_messages_ros2.rolling.lifecycle_msgs.msg import state_pb2 as _state_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetAvailableStatesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetAvailableStatesResponse(_message.Message):
    __slots__ = ("available_states",)
    AVAILABLE_STATES_FIELD_NUMBER: _ClassVar[int]
    available_states: _containers.RepeatedCompositeFieldContainer[_state_pb2.State]
    def __init__(self, available_states: _Optional[_Iterable[_Union[_state_pb2.State, _Mapping]]] = ...) -> None: ...
