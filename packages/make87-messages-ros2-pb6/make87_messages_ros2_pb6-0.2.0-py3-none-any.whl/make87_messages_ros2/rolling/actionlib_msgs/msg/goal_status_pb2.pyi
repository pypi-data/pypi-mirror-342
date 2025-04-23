from make87_messages_ros2.rolling.actionlib_msgs.msg import goal_id_pb2 as _goal_id_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GoalStatus(_message.Message):
    __slots__ = ("goal_id", "status", "text")
    GOAL_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    goal_id: _goal_id_pb2.GoalID
    status: int
    text: str
    def __init__(self, goal_id: _Optional[_Union[_goal_id_pb2.GoalID, _Mapping]] = ..., status: _Optional[int] = ..., text: _Optional[str] = ...) -> None: ...
