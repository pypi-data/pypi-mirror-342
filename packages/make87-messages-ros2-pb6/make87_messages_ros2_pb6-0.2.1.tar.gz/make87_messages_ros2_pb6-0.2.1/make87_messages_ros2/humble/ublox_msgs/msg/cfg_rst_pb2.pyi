from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CfgRST(_message.Message):
    __slots__ = ("header", "nav_bbr_mask", "reset_mode", "reserved1")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAV_BBR_MASK_FIELD_NUMBER: _ClassVar[int]
    RESET_MODE_FIELD_NUMBER: _ClassVar[int]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    nav_bbr_mask: int
    reset_mode: int
    reserved1: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., nav_bbr_mask: _Optional[int] = ..., reset_mode: _Optional[int] = ..., reserved1: _Optional[int] = ...) -> None: ...
