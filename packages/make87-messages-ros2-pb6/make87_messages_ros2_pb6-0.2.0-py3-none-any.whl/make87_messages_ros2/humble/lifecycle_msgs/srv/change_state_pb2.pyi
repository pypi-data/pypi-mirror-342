from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.lifecycle_msgs.msg import transition_pb2 as _transition_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChangeStateRequest(_message.Message):
    __slots__ = ("header", "transition")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TRANSITION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    transition: _transition_pb2.Transition
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., transition: _Optional[_Union[_transition_pb2.Transition, _Mapping]] = ...) -> None: ...

class ChangeStateResponse(_message.Message):
    __slots__ = ("header", "success")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ...) -> None: ...
