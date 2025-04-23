from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OutcomeRequest(_message.Message):
    __slots__ = ("header", "outcome", "target")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    OUTCOME_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    outcome: int
    target: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., outcome: _Optional[int] = ..., target: _Optional[str] = ...) -> None: ...
