from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClientMapStartRequest(_message.Message):
    __slots__ = ("header", "recording_name", "client_map_name")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RECORDING_NAME_FIELD_NUMBER: _ClassVar[int]
    CLIENT_MAP_NAME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    recording_name: str
    client_map_name: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., recording_name: _Optional[str] = ..., client_map_name: _Optional[str] = ...) -> None: ...

class ClientMapStartResponse(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...
