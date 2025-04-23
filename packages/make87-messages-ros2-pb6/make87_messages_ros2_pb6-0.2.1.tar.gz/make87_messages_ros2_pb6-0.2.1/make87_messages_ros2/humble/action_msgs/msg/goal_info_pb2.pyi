from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.humble.unique_identifier_msgs.msg import uuid_pb2 as _uuid_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GoalInfo(_message.Message):
    __slots__ = ("header", "goal_id", "stamp")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    GOAL_ID_FIELD_NUMBER: _ClassVar[int]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    goal_id: _uuid_pb2.UUID
    stamp: _time_pb2.Time
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., goal_id: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ...) -> None: ...
