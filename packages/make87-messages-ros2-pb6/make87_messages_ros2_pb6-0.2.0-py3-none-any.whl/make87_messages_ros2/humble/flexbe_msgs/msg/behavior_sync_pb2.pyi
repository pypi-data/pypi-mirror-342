from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BehaviorSync(_message.Message):
    __slots__ = ("header", "behavior_id", "current_state_checksum")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BEHAVIOR_ID_FIELD_NUMBER: _ClassVar[int]
    CURRENT_STATE_CHECKSUM_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    behavior_id: int
    current_state_checksum: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., behavior_id: _Optional[int] = ..., current_state_checksum: _Optional[int] = ...) -> None: ...
