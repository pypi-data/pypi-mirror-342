from make87_messages_ros2.rolling.tuw_graph_msgs.msg import graph_pb2 as _graph_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetGraphRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetGraphResponse(_message.Message):
    __slots__ = ("graph",)
    GRAPH_FIELD_NUMBER: _ClassVar[int]
    graph: _graph_pb2.Graph
    def __init__(self, graph: _Optional[_Union[_graph_pb2.Graph, _Mapping]] = ...) -> None: ...
