from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.plansys2_msgs.msg import node_pb2 as _node_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ExistNodeRequest(_message.Message):
    __slots__ = ("header", "node")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NODE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    node: _node_pb2.Node
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., node: _Optional[_Union[_node_pb2.Node, _Mapping]] = ...) -> None: ...

class ExistNodeResponse(_message.Message):
    __slots__ = ("header", "exist")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    EXIST_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    exist: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., exist: bool = ...) -> None: ...
