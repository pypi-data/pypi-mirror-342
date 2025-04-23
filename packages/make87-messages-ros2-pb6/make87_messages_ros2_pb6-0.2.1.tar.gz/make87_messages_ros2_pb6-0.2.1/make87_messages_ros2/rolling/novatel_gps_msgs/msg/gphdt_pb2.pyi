from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Gphdt(_message.Message):
    __slots__ = ("header", "message_id", "heading", "t")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    HEADING_FIELD_NUMBER: _ClassVar[int]
    T_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    message_id: str
    heading: float
    t: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., message_id: _Optional[str] = ..., heading: _Optional[float] = ..., t: _Optional[str] = ...) -> None: ...
