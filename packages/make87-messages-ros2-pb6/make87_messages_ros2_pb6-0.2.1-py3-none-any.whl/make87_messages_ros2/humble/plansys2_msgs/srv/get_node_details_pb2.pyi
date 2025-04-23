from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.plansys2_msgs.msg import node_pb2 as _node_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetNodeDetailsRequest(_message.Message):
    __slots__ = ("header", "expression")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    expression: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., expression: _Optional[str] = ...) -> None: ...

class GetNodeDetailsResponse(_message.Message):
    __slots__ = ("header", "success", "node", "error_info")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    NODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_INFO_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    node: _node_pb2.Node
    error_info: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., node: _Optional[_Union[_node_pb2.Node, _Mapping]] = ..., error_info: _Optional[str] = ...) -> None: ...
