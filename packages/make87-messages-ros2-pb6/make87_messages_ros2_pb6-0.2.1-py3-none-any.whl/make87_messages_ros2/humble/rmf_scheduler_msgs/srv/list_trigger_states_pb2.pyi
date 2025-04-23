from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_scheduler_msgs.msg import trigger_state_pb2 as _trigger_state_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListTriggerStatesRequest(_message.Message):
    __slots__ = ("header", "modified_after")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_AFTER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    modified_after: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., modified_after: _Optional[int] = ...) -> None: ...

class ListTriggerStatesResponse(_message.Message):
    __slots__ = ("header", "success", "message", "triggers")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TRIGGERS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    message: str
    triggers: _containers.RepeatedCompositeFieldContainer[_trigger_state_pb2.TriggerState]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., message: _Optional[str] = ..., triggers: _Optional[_Iterable[_Union[_trigger_state_pb2.TriggerState, _Mapping]]] = ...) -> None: ...
