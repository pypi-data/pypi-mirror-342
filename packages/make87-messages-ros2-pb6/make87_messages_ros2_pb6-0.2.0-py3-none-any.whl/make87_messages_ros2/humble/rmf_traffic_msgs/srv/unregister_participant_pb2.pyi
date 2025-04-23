from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UnregisterParticipantRequest(_message.Message):
    __slots__ = ("header", "participant_id")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANT_ID_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    participant_id: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., participant_id: _Optional[int] = ...) -> None: ...

class UnregisterParticipantResponse(_message.Message):
    __slots__ = ("header", "confirmation", "error")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CONFIRMATION_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    confirmation: bool
    error: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., confirmation: bool = ..., error: _Optional[str] = ...) -> None: ...
