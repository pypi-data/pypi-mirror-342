from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.soccer_object_msgs.msg import field_line_pb2 as _field_line_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FieldLineArray(_message.Message):
    __slots__ = ("header", "lines")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LINES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    lines: _containers.RepeatedCompositeFieldContainer[_field_line_pb2.FieldLine]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., lines: _Optional[_Iterable[_Union[_field_line_pb2.FieldLine, _Mapping]]] = ...) -> None: ...
