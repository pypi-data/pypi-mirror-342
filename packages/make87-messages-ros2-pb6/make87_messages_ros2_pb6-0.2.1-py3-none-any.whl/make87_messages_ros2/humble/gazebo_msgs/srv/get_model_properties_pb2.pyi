from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetModelPropertiesRequest(_message.Message):
    __slots__ = ("header", "model_name")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    model_name: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., model_name: _Optional[str] = ...) -> None: ...

class GetModelPropertiesResponse(_message.Message):
    __slots__ = ("header", "parent_model_name", "canonical_body_name", "body_names", "geom_names", "joint_names", "child_model_names", "is_static", "success", "status_message")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PARENT_MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    CANONICAL_BODY_NAME_FIELD_NUMBER: _ClassVar[int]
    BODY_NAMES_FIELD_NUMBER: _ClassVar[int]
    GEOM_NAMES_FIELD_NUMBER: _ClassVar[int]
    JOINT_NAMES_FIELD_NUMBER: _ClassVar[int]
    CHILD_MODEL_NAMES_FIELD_NUMBER: _ClassVar[int]
    IS_STATIC_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    parent_model_name: str
    canonical_body_name: str
    body_names: _containers.RepeatedScalarFieldContainer[str]
    geom_names: _containers.RepeatedScalarFieldContainer[str]
    joint_names: _containers.RepeatedScalarFieldContainer[str]
    child_model_names: _containers.RepeatedScalarFieldContainer[str]
    is_static: bool
    success: bool
    status_message: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., parent_model_name: _Optional[str] = ..., canonical_body_name: _Optional[str] = ..., body_names: _Optional[_Iterable[str]] = ..., geom_names: _Optional[_Iterable[str]] = ..., joint_names: _Optional[_Iterable[str]] = ..., child_model_names: _Optional[_Iterable[str]] = ..., is_static: bool = ..., success: bool = ..., status_message: _Optional[str] = ...) -> None: ...
