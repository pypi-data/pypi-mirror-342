from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VideoRecord(_message.Message):
    __slots__ = ("header", "start", "stop", "format", "save_filename")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    STOP_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    SAVE_FILENAME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    start: bool
    stop: bool
    format: str
    save_filename: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., start: bool = ..., stop: bool = ..., format: _Optional[str] = ..., save_filename: _Optional[str] = ...) -> None: ...
