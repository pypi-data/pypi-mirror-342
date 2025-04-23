from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class JointsIWS(_message.Message):
    __slots__ = ("header", "type_steering", "type_revolute", "steering", "revolute")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TYPE_STEERING_FIELD_NUMBER: _ClassVar[int]
    TYPE_REVOLUTE_FIELD_NUMBER: _ClassVar[int]
    STEERING_FIELD_NUMBER: _ClassVar[int]
    REVOLUTE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    type_steering: str
    type_revolute: str
    steering: _containers.RepeatedScalarFieldContainer[float]
    revolute: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., type_steering: _Optional[str] = ..., type_revolute: _Optional[str] = ..., steering: _Optional[_Iterable[float]] = ..., revolute: _Optional[_Iterable[float]] = ...) -> None: ...
