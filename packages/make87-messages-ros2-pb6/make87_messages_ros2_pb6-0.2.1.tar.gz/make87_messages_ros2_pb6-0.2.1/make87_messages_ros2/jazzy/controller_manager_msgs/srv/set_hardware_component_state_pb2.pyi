from make87_messages_ros2.jazzy.lifecycle_msgs.msg import state_pb2 as _state_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetHardwareComponentStateRequest(_message.Message):
    __slots__ = ("name", "target_state")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TARGET_STATE_FIELD_NUMBER: _ClassVar[int]
    name: str
    target_state: _state_pb2.State
    def __init__(self, name: _Optional[str] = ..., target_state: _Optional[_Union[_state_pb2.State, _Mapping]] = ...) -> None: ...

class SetHardwareComponentStateResponse(_message.Message):
    __slots__ = ("ok", "state")
    OK_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    ok: bool
    state: _state_pb2.State
    def __init__(self, ok: bool = ..., state: _Optional[_Union[_state_pb2.State, _Mapping]] = ...) -> None: ...
