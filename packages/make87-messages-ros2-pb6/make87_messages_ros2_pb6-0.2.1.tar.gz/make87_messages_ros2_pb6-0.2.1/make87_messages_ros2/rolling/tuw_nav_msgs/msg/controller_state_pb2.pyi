from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ControllerState(_message.Message):
    __slots__ = ("header", "state", "progress", "progress_in_relation_to", "info")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_IN_RELATION_TO_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    state: int
    progress: int
    progress_in_relation_to: int
    info: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., state: _Optional[int] = ..., progress: _Optional[int] = ..., progress_in_relation_to: _Optional[int] = ..., info: _Optional[str] = ...) -> None: ...
