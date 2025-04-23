from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SubscribersRequest(_message.Message):
    __slots__ = ("header", "topic")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    topic: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., topic: _Optional[str] = ...) -> None: ...

class SubscribersResponse(_message.Message):
    __slots__ = ("header", "subscribers")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIBERS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    subscribers: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., subscribers: _Optional[_Iterable[str]] = ...) -> None: ...
