from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BlockadeReached(_message.Message):
    __slots__ = ("header", "participant", "reservation", "checkpoint")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANT_FIELD_NUMBER: _ClassVar[int]
    RESERVATION_FIELD_NUMBER: _ClassVar[int]
    CHECKPOINT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    participant: int
    reservation: int
    checkpoint: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., participant: _Optional[int] = ..., reservation: _Optional[int] = ..., checkpoint: _Optional[int] = ...) -> None: ...
