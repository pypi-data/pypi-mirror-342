from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.action_msgs.msg import goal_info_pb2 as _goal_info_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GoalStatus(_message.Message):
    __slots__ = ("header", "goal_info", "status")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    GOAL_INFO_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    goal_info: _goal_info_pb2.GoalInfo
    status: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., goal_info: _Optional[_Union[_goal_info_pb2.GoalInfo, _Mapping]] = ..., status: _Optional[int] = ...) -> None: ...
