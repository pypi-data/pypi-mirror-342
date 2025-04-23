from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LIDinputstateMsg(_message.Message):
    __slots__ = ("header", "ros2_header", "version_number", "system_counter", "input_state", "active_fieldset", "time_state", "year", "month", "day", "hour", "minute", "second", "microsecond")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    VERSION_NUMBER_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_COUNTER_FIELD_NUMBER: _ClassVar[int]
    INPUT_STATE_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELDSET_FIELD_NUMBER: _ClassVar[int]
    TIME_STATE_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    MONTH_FIELD_NUMBER: _ClassVar[int]
    DAY_FIELD_NUMBER: _ClassVar[int]
    HOUR_FIELD_NUMBER: _ClassVar[int]
    MINUTE_FIELD_NUMBER: _ClassVar[int]
    SECOND_FIELD_NUMBER: _ClassVar[int]
    MICROSECOND_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    version_number: int
    system_counter: int
    input_state: _containers.RepeatedScalarFieldContainer[int]
    active_fieldset: int
    time_state: int
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    microsecond: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., version_number: _Optional[int] = ..., system_counter: _Optional[int] = ..., input_state: _Optional[_Iterable[int]] = ..., active_fieldset: _Optional[int] = ..., time_state: _Optional[int] = ..., year: _Optional[int] = ..., month: _Optional[int] = ..., day: _Optional[int] = ..., hour: _Optional[int] = ..., minute: _Optional[int] = ..., second: _Optional[int] = ..., microsecond: _Optional[int] = ...) -> None: ...
