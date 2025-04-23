from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Ack(_message.Message):
    __slots__ = ("header", "cls_id", "msg_id")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CLS_ID_FIELD_NUMBER: _ClassVar[int]
    MSG_ID_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    cls_id: int
    msg_id: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., cls_id: _Optional[int] = ..., msg_id: _Optional[int] = ...) -> None: ...
