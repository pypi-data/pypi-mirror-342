from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Quality(_message.Message):
    __slots__ = ("header", "ros2_header", "messages_received", "messages_missed", "total_length", "message_lengths", "latency_avg", "latency_measurements")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_RECEIVED_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_MISSED_FIELD_NUMBER: _ClassVar[int]
    TOTAL_LENGTH_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_LENGTHS_FIELD_NUMBER: _ClassVar[int]
    LATENCY_AVG_FIELD_NUMBER: _ClassVar[int]
    LATENCY_MEASUREMENTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    messages_received: int
    messages_missed: int
    total_length: int
    message_lengths: _containers.RepeatedScalarFieldContainer[int]
    latency_avg: float
    latency_measurements: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., messages_received: _Optional[int] = ..., messages_missed: _Optional[int] = ..., total_length: _Optional[int] = ..., message_lengths: _Optional[_Iterable[int]] = ..., latency_avg: _Optional[float] = ..., latency_measurements: _Optional[_Iterable[float]] = ...) -> None: ...
