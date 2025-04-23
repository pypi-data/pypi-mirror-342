from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_scheduler_msgs.msg import schedule_pb2 as _schedule_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateScheduleRequest(_message.Message):
    __slots__ = ("header", "schedule")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    schedule: _schedule_pb2.Schedule
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., schedule: _Optional[_Union[_schedule_pb2.Schedule, _Mapping]] = ...) -> None: ...

class CreateScheduleResponse(_message.Message):
    __slots__ = ("header", "success", "message")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    message: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., message: _Optional[str] = ...) -> None: ...
