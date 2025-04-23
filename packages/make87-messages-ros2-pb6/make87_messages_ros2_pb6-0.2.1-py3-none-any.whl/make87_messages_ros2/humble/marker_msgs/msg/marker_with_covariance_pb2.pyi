from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.marker_msgs.msg import marker_pb2 as _marker_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MarkerWithCovariance(_message.Message):
    __slots__ = ("header", "marker", "covariance")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MARKER_FIELD_NUMBER: _ClassVar[int]
    COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    marker: _marker_pb2.Marker
    covariance: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., marker: _Optional[_Union[_marker_pb2.Marker, _Mapping]] = ..., covariance: _Optional[_Iterable[float]] = ...) -> None: ...
