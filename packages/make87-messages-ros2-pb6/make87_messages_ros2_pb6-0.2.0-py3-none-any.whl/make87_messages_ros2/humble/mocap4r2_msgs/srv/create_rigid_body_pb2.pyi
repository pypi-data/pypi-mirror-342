from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateRigidBodyRequest(_message.Message):
    __slots__ = ("header", "rigid_body_name", "link_parent", "markers")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RIGID_BODY_NAME_FIELD_NUMBER: _ClassVar[int]
    LINK_PARENT_FIELD_NUMBER: _ClassVar[int]
    MARKERS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    rigid_body_name: str
    link_parent: str
    markers: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., rigid_body_name: _Optional[str] = ..., link_parent: _Optional[str] = ..., markers: _Optional[_Iterable[int]] = ...) -> None: ...

class CreateRigidBodyResponse(_message.Message):
    __slots__ = ("header", "success")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ...) -> None: ...
