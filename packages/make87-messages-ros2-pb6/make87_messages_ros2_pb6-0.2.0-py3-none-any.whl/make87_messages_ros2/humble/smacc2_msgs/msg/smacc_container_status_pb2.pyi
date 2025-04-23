from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SmaccContainerStatus(_message.Message):
    __slots__ = ("header", "ros2_header", "path", "initial_states", "active_states", "local_data", "info")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    INITIAL_STATES_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_STATES_FIELD_NUMBER: _ClassVar[int]
    LOCAL_DATA_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    path: str
    initial_states: _containers.RepeatedScalarFieldContainer[str]
    active_states: _containers.RepeatedScalarFieldContainer[str]
    local_data: str
    info: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., path: _Optional[str] = ..., initial_states: _Optional[_Iterable[str]] = ..., active_states: _Optional[_Iterable[str]] = ..., local_data: _Optional[str] = ..., info: _Optional[str] = ...) -> None: ...
