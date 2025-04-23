from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OpenBlackboardStreamRequest(_message.Message):
    __slots__ = ("header", "variables", "filter_on_visited_path", "with_activity_stream")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VARIABLES_FIELD_NUMBER: _ClassVar[int]
    FILTER_ON_VISITED_PATH_FIELD_NUMBER: _ClassVar[int]
    WITH_ACTIVITY_STREAM_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    variables: _containers.RepeatedScalarFieldContainer[str]
    filter_on_visited_path: bool
    with_activity_stream: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., variables: _Optional[_Iterable[str]] = ..., filter_on_visited_path: bool = ..., with_activity_stream: bool = ...) -> None: ...

class OpenBlackboardStreamResponse(_message.Message):
    __slots__ = ("header", "topic")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    topic: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., topic: _Optional[str] = ...) -> None: ...
