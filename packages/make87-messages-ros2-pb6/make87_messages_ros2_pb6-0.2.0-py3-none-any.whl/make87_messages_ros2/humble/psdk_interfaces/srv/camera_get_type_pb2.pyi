from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CameraGetTypeRequest(_message.Message):
    __slots__ = ("header", "payload_index")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_INDEX_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    payload_index: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., payload_index: _Optional[int] = ...) -> None: ...

class CameraGetTypeResponse(_message.Message):
    __slots__ = ("header", "success", "camera_type")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    CAMERA_TYPE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    camera_type: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., camera_type: _Optional[str] = ...) -> None: ...
