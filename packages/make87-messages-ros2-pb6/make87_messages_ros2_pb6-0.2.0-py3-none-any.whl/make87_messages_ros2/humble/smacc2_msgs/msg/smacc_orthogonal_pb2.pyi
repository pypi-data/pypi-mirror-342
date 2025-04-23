from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SmaccOrthogonal(_message.Message):
    __slots__ = ("header", "name", "client_behavior_names", "client_names")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CLIENT_BEHAVIOR_NAMES_FIELD_NUMBER: _ClassVar[int]
    CLIENT_NAMES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    client_behavior_names: _containers.RepeatedScalarFieldContainer[str]
    client_names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., client_behavior_names: _Optional[_Iterable[str]] = ..., client_names: _Optional[_Iterable[str]] = ...) -> None: ...
