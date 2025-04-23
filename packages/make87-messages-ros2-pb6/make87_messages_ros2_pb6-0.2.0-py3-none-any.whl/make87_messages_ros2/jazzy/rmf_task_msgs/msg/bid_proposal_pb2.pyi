from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BidProposal(_message.Message):
    __slots__ = ("fleet_name", "expected_robot_name", "prev_cost", "new_cost", "finish_time")
    FLEET_NAME_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_ROBOT_NAME_FIELD_NUMBER: _ClassVar[int]
    PREV_COST_FIELD_NUMBER: _ClassVar[int]
    NEW_COST_FIELD_NUMBER: _ClassVar[int]
    FINISH_TIME_FIELD_NUMBER: _ClassVar[int]
    fleet_name: str
    expected_robot_name: str
    prev_cost: float
    new_cost: float
    finish_time: _time_pb2.Time
    def __init__(self, fleet_name: _Optional[str] = ..., expected_robot_name: _Optional[str] = ..., prev_cost: _Optional[float] = ..., new_cost: _Optional[float] = ..., finish_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ...) -> None: ...
