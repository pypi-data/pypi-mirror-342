from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Network(_message.Message):
    __slots__ = ("header", "type", "essid", "mac", "mode", "frequency", "encryption")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ESSID_FIELD_NUMBER: _ClassVar[int]
    MAC_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    type: str
    essid: str
    mac: str
    mode: str
    frequency: str
    encryption: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., type: _Optional[str] = ..., essid: _Optional[str] = ..., mac: _Optional[str] = ..., mode: _Optional[str] = ..., frequency: _Optional[str] = ..., encryption: bool = ...) -> None: ...
