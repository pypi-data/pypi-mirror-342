from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_scheduler_msgs.msg import trigger_pb2 as _trigger_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateTriggerRequest(_message.Message):
    __slots__ = ("header", "trigger")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    trigger: _trigger_pb2.Trigger
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., trigger: _Optional[_Union[_trigger_pb2.Trigger, _Mapping]] = ...) -> None: ...

class CreateTriggerResponse(_message.Message):
    __slots__ = ("header", "success", "message")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    message: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., message: _Optional[str] = ...) -> None: ...
