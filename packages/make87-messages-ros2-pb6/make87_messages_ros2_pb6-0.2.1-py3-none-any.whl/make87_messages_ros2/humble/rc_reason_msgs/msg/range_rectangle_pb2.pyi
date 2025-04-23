from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rc_reason_msgs.msg import rectangle_pb2 as _rectangle_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RangeRectangle(_message.Message):
    __slots__ = ("header", "min_dimensions", "max_dimensions")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MIN_DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    MAX_DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    min_dimensions: _rectangle_pb2.Rectangle
    max_dimensions: _rectangle_pb2.Rectangle
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., min_dimensions: _Optional[_Union[_rectangle_pb2.Rectangle, _Mapping]] = ..., max_dimensions: _Optional[_Union[_rectangle_pb2.Rectangle, _Mapping]] = ...) -> None: ...
