from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MotorOverCurrentConfigCmd(_message.Message):
    __slots__ = ("header", "confirm", "over_current")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CONFIRM_FIELD_NUMBER: _ClassVar[int]
    OVER_CURRENT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    confirm: bool
    over_current: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., confirm: bool = ..., over_current: _Optional[int] = ...) -> None: ...
