from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PublishedTime(_message.Message):
    __slots__ = ("header", "published_stamp")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PUBLISHED_STAMP_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    published_stamp: _time_pb2.Time
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., published_stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ...) -> None: ...
