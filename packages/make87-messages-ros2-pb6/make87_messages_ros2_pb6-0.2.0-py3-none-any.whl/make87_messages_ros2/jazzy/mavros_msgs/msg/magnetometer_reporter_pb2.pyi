from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MagnetometerReporter(_message.Message):
    __slots__ = ("header", "report", "confidence")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    REPORT_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    report: int
    confidence: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., report: _Optional[int] = ..., confidence: _Optional[float] = ...) -> None: ...
