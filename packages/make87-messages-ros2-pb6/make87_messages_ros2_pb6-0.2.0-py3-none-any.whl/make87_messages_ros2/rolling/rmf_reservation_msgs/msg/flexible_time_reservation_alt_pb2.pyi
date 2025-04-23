from make87_messages_ros2.rolling.builtin_interfaces.msg import duration_pb2 as _duration_pb2
from make87_messages_ros2.rolling.rmf_reservation_msgs.msg import start_time_range_pb2 as _start_time_range_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FlexibleTimeReservationAlt(_message.Message):
    __slots__ = ("resource_name", "cost", "start_time", "has_end", "duration")
    RESOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    COST_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    HAS_END_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    resource_name: str
    cost: float
    start_time: _start_time_range_pb2.StartTimeRange
    has_end: bool
    duration: _duration_pb2.Duration
    def __init__(self, resource_name: _Optional[str] = ..., cost: _Optional[float] = ..., start_time: _Optional[_Union[_start_time_range_pb2.StartTimeRange, _Mapping]] = ..., has_end: bool = ..., duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...
