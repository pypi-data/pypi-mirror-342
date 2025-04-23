from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DistanceToDestination(_message.Message):
    __slots__ = ("header", "msg_counter", "distance")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MSG_COUNTER_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    msg_counter: int
    distance: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., msg_counter: _Optional[int] = ..., distance: _Optional[float] = ...) -> None: ...
