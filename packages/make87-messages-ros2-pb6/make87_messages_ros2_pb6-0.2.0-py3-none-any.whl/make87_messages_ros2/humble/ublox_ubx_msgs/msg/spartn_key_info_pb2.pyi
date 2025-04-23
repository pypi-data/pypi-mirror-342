from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SpartnKeyInfo(_message.Message):
    __slots__ = ("header", "reserved1", "key_length_bytes", "valid_from_wno", "valid_from_tow")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    KEY_LENGTH_BYTES_FIELD_NUMBER: _ClassVar[int]
    VALID_FROM_WNO_FIELD_NUMBER: _ClassVar[int]
    VALID_FROM_TOW_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    reserved1: int
    key_length_bytes: int
    valid_from_wno: int
    valid_from_tow: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., reserved1: _Optional[int] = ..., key_length_bytes: _Optional[int] = ..., valid_from_wno: _Optional[int] = ..., valid_from_tow: _Optional[int] = ...) -> None: ...
