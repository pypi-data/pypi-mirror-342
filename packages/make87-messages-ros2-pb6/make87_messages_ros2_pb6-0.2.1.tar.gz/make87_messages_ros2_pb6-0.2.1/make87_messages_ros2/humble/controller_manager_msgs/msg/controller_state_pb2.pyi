from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.controller_manager_msgs.msg import chain_connection_pb2 as _chain_connection_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ControllerState(_message.Message):
    __slots__ = ("header", "name", "state", "type", "claimed_interfaces", "required_command_interfaces", "required_state_interfaces", "is_chainable", "is_chained", "reference_interfaces", "chain_connections")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CLAIMED_INTERFACES_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_COMMAND_INTERFACES_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_STATE_INTERFACES_FIELD_NUMBER: _ClassVar[int]
    IS_CHAINABLE_FIELD_NUMBER: _ClassVar[int]
    IS_CHAINED_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_INTERFACES_FIELD_NUMBER: _ClassVar[int]
    CHAIN_CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    state: str
    type: str
    claimed_interfaces: _containers.RepeatedScalarFieldContainer[str]
    required_command_interfaces: _containers.RepeatedScalarFieldContainer[str]
    required_state_interfaces: _containers.RepeatedScalarFieldContainer[str]
    is_chainable: bool
    is_chained: bool
    reference_interfaces: _containers.RepeatedScalarFieldContainer[str]
    chain_connections: _containers.RepeatedCompositeFieldContainer[_chain_connection_pb2.ChainConnection]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., state: _Optional[str] = ..., type: _Optional[str] = ..., claimed_interfaces: _Optional[_Iterable[str]] = ..., required_command_interfaces: _Optional[_Iterable[str]] = ..., required_state_interfaces: _Optional[_Iterable[str]] = ..., is_chainable: bool = ..., is_chained: bool = ..., reference_interfaces: _Optional[_Iterable[str]] = ..., chain_connections: _Optional[_Iterable[_Union[_chain_connection_pb2.ChainConnection, _Mapping]]] = ...) -> None: ...
