from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CfgMSG(_message.Message):
    __slots__ = ("header", "msg_class", "msg_id", "rate")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MSG_CLASS_FIELD_NUMBER: _ClassVar[int]
    MSG_ID_FIELD_NUMBER: _ClassVar[int]
    RATE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    msg_class: int
    msg_id: int
    rate: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., msg_class: _Optional[int] = ..., msg_id: _Optional[int] = ..., rate: _Optional[int] = ...) -> None: ...
