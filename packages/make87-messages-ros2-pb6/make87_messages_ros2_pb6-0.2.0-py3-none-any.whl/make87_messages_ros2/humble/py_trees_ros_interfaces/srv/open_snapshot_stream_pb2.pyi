from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.py_trees_ros_interfaces.msg import snapshot_stream_parameters_pb2 as _snapshot_stream_parameters_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OpenSnapshotStreamRequest(_message.Message):
    __slots__ = ("header", "topic_name", "parameters")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TOPIC_NAME_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    topic_name: str
    parameters: _snapshot_stream_parameters_pb2.SnapshotStreamParameters
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., topic_name: _Optional[str] = ..., parameters: _Optional[_Union[_snapshot_stream_parameters_pb2.SnapshotStreamParameters, _Mapping]] = ...) -> None: ...

class OpenSnapshotStreamResponse(_message.Message):
    __slots__ = ("header", "topic_name")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TOPIC_NAME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    topic_name: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., topic_name: _Optional[str] = ...) -> None: ...
