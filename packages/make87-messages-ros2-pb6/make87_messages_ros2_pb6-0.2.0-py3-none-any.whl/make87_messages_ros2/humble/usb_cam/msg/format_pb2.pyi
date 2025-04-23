from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Format(_message.Message):
    __slots__ = ("header", "pixel_format", "width", "height", "fps")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PIXEL_FORMAT_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    FPS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    pixel_format: str
    width: int
    height: int
    fps: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., pixel_format: _Optional[str] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., fps: _Optional[float] = ...) -> None: ...
