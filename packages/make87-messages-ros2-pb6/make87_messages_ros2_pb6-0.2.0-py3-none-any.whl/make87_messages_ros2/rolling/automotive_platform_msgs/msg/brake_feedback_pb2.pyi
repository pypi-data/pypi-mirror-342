from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BrakeFeedback(_message.Message):
    __slots__ = ("header", "brake_pedal")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BRAKE_PEDAL_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    brake_pedal: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., brake_pedal: _Optional[float] = ...) -> None: ...
