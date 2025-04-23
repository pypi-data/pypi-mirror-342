from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetJointPropertiesRequest(_message.Message):
    __slots__ = ("header", "joint_name")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    JOINT_NAME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    joint_name: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., joint_name: _Optional[str] = ...) -> None: ...

class GetJointPropertiesResponse(_message.Message):
    __slots__ = ("header", "type", "damping", "position", "rate", "success", "status_message")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DAMPING_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    RATE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    type: int
    damping: _containers.RepeatedScalarFieldContainer[float]
    position: _containers.RepeatedScalarFieldContainer[float]
    rate: _containers.RepeatedScalarFieldContainer[float]
    success: bool
    status_message: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., type: _Optional[int] = ..., damping: _Optional[_Iterable[float]] = ..., position: _Optional[_Iterable[float]] = ..., rate: _Optional[_Iterable[float]] = ..., success: bool = ..., status_message: _Optional[str] = ...) -> None: ...
