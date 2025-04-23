from make87_messages_ros2.rolling.diagnostic_msgs.msg import diagnostic_status_pb2 as _diagnostic_status_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DiagnosticArray(_message.Message):
    __slots__ = ("header", "status")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    status: _containers.RepeatedCompositeFieldContainer[_diagnostic_status_pb2.DiagnosticStatus]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., status: _Optional[_Iterable[_Union[_diagnostic_status_pb2.DiagnosticStatus, _Mapping]]] = ...) -> None: ...
