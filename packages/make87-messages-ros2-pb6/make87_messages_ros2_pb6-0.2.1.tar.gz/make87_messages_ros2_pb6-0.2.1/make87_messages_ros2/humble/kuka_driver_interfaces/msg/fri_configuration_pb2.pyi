from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FriConfiguration(_message.Message):
    __slots__ = ("header", "receive_multiplier", "send_period_ms")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RECEIVE_MULTIPLIER_FIELD_NUMBER: _ClassVar[int]
    SEND_PERIOD_MS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    receive_multiplier: int
    send_period_ms: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., receive_multiplier: _Optional[int] = ..., send_period_ms: _Optional[int] = ...) -> None: ...
