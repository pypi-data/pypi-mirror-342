from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ParamPullRequest(_message.Message):
    __slots__ = ("header", "force_pull")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FORCE_PULL_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    force_pull: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., force_pull: bool = ...) -> None: ...

class ParamPullResponse(_message.Message):
    __slots__ = ("header", "success", "param_received")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    PARAM_RECEIVED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    param_received: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., param_received: _Optional[int] = ...) -> None: ...
