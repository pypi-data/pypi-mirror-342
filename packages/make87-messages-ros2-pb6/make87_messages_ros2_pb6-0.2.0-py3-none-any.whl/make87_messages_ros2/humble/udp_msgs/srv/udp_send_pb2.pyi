from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UdpSendRequest(_message.Message):
    __slots__ = ("header", "local_address", "local_port", "remote_address", "remote_port", "data")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LOCAL_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    LOCAL_PORT_FIELD_NUMBER: _ClassVar[int]
    REMOTE_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    REMOTE_PORT_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    local_address: str
    local_port: int
    remote_address: str
    remote_port: int
    data: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., local_address: _Optional[str] = ..., local_port: _Optional[int] = ..., remote_address: _Optional[str] = ..., remote_port: _Optional[int] = ..., data: _Optional[_Iterable[int]] = ...) -> None: ...

class UdpSendResponse(_message.Message):
    __slots__ = ("header", "sent")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SENT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    sent: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., sent: bool = ...) -> None: ...
