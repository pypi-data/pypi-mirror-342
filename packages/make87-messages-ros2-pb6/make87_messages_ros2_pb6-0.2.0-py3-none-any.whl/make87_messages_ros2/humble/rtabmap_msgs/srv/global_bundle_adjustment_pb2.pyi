from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GlobalBundleAdjustmentRequest(_message.Message):
    __slots__ = ("header", "type", "iterations", "pixel_variance", "voc_matches")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ITERATIONS_FIELD_NUMBER: _ClassVar[int]
    PIXEL_VARIANCE_FIELD_NUMBER: _ClassVar[int]
    VOC_MATCHES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    type: int
    iterations: int
    pixel_variance: float
    voc_matches: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., type: _Optional[int] = ..., iterations: _Optional[int] = ..., pixel_variance: _Optional[float] = ..., voc_matches: bool = ...) -> None: ...

class GlobalBundleAdjustmentResponse(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...
