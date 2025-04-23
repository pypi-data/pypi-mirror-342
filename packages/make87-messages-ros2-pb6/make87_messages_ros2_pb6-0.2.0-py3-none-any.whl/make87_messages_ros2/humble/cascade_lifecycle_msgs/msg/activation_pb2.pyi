from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Activation(_message.Message):
    __slots__ = ("header", "operation_type", "activator", "activation")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    OPERATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACTIVATOR_FIELD_NUMBER: _ClassVar[int]
    ACTIVATION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    operation_type: int
    activator: str
    activation: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., operation_type: _Optional[int] = ..., activator: _Optional[str] = ..., activation: _Optional[str] = ...) -> None: ...
