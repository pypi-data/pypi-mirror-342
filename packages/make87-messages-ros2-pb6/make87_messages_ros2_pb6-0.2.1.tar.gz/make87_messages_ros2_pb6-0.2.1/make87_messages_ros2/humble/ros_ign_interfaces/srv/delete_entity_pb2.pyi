from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.ros_gz_interfaces.msg import entity_pb2 as _entity_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DeleteEntityRequest(_message.Message):
    __slots__ = ("header", "entity")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    entity: _entity_pb2.Entity
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., entity: _Optional[_Union[_entity_pb2.Entity, _Mapping]] = ...) -> None: ...

class DeleteEntityResponse(_message.Message):
    __slots__ = ("header", "success")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ...) -> None: ...
