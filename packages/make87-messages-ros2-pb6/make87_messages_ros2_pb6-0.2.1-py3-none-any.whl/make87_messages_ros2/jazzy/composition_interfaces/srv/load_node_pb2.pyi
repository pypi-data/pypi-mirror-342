from make87_messages_ros2.jazzy.rcl_interfaces.msg import parameter_pb2 as _parameter_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LoadNodeRequest(_message.Message):
    __slots__ = ("package_name", "plugin_name", "node_name", "node_namespace", "log_level", "remap_rules", "parameters", "extra_arguments")
    PACKAGE_NAME_FIELD_NUMBER: _ClassVar[int]
    PLUGIN_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    LOG_LEVEL_FIELD_NUMBER: _ClassVar[int]
    REMAP_RULES_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    EXTRA_ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
    package_name: str
    plugin_name: str
    node_name: str
    node_namespace: str
    log_level: int
    remap_rules: _containers.RepeatedScalarFieldContainer[str]
    parameters: _containers.RepeatedCompositeFieldContainer[_parameter_pb2.Parameter]
    extra_arguments: _containers.RepeatedCompositeFieldContainer[_parameter_pb2.Parameter]
    def __init__(self, package_name: _Optional[str] = ..., plugin_name: _Optional[str] = ..., node_name: _Optional[str] = ..., node_namespace: _Optional[str] = ..., log_level: _Optional[int] = ..., remap_rules: _Optional[_Iterable[str]] = ..., parameters: _Optional[_Iterable[_Union[_parameter_pb2.Parameter, _Mapping]]] = ..., extra_arguments: _Optional[_Iterable[_Union[_parameter_pb2.Parameter, _Mapping]]] = ...) -> None: ...

class LoadNodeResponse(_message.Message):
    __slots__ = ("success", "error_message", "full_node_name", "unique_id")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    FULL_NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error_message: str
    full_node_name: str
    unique_id: int
    def __init__(self, success: bool = ..., error_message: _Optional[str] = ..., full_node_name: _Optional[str] = ..., unique_id: _Optional[int] = ...) -> None: ...
