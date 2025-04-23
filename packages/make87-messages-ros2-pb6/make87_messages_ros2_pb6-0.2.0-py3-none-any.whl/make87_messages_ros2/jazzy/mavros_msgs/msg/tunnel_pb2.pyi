from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Tunnel(_message.Message):
    __slots__ = ("target_system", "target_component", "payload_type", "payload_length", "payload")
    TARGET_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    TARGET_COMPONENT_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_LENGTH_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    target_system: int
    target_component: int
    payload_type: int
    payload_length: int
    payload: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, target_system: _Optional[int] = ..., target_component: _Optional[int] = ..., payload_type: _Optional[int] = ..., payload_length: _Optional[int] = ..., payload: _Optional[_Iterable[int]] = ...) -> None: ...
