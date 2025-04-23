from make87_messages_ros2.jazzy.fuse_msgs.msg import serialized_graph_pb2 as _serialized_graph_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetGraphRequest(_message.Message):
    __slots__ = ("graph",)
    GRAPH_FIELD_NUMBER: _ClassVar[int]
    graph: _serialized_graph_pb2.SerializedGraph
    def __init__(self, graph: _Optional[_Union[_serialized_graph_pb2.SerializedGraph, _Mapping]] = ...) -> None: ...

class SetGraphResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...
