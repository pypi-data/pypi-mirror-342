from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RFBand(_message.Message):
    __slots__ = ("header", "frequency", "bandwidth", "info")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    BANDWIDTH_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    frequency: int
    bandwidth: int
    info: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., frequency: _Optional[int] = ..., bandwidth: _Optional[int] = ..., info: _Optional[int] = ...) -> None: ...
