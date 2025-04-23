from make87_messages_ros2.rolling.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TimeStamped(_message.Message):
    __slots__ = ("header", "value")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    value: _time_pb2.Time
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., value: _Optional[_Union[_time_pb2.Time, _Mapping]] = ...) -> None: ...
