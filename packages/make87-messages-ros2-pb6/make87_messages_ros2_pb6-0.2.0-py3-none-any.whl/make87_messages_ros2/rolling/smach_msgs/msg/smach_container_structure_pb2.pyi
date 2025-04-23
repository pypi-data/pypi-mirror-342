from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SmachContainerStructure(_message.Message):
    __slots__ = ("header", "path", "children", "internal_outcomes", "outcomes_from", "outcomes_to", "container_outcomes")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    CHILDREN_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_OUTCOMES_FIELD_NUMBER: _ClassVar[int]
    OUTCOMES_FROM_FIELD_NUMBER: _ClassVar[int]
    OUTCOMES_TO_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_OUTCOMES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    path: str
    children: _containers.RepeatedScalarFieldContainer[str]
    internal_outcomes: _containers.RepeatedScalarFieldContainer[str]
    outcomes_from: _containers.RepeatedScalarFieldContainer[str]
    outcomes_to: _containers.RepeatedScalarFieldContainer[str]
    container_outcomes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., path: _Optional[str] = ..., children: _Optional[_Iterable[str]] = ..., internal_outcomes: _Optional[_Iterable[str]] = ..., outcomes_from: _Optional[_Iterable[str]] = ..., outcomes_to: _Optional[_Iterable[str]] = ..., container_outcomes: _Optional[_Iterable[str]] = ...) -> None: ...
