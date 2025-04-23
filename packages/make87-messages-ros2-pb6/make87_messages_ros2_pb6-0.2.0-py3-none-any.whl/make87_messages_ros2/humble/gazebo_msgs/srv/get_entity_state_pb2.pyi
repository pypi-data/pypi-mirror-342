from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.gazebo_msgs.msg import entity_state_pb2 as _entity_state_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetEntityStateRequest(_message.Message):
    __slots__ = ("header", "name", "reference_frame")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_FRAME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    reference_frame: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., reference_frame: _Optional[str] = ...) -> None: ...

class GetEntityStateResponse(_message.Message):
    __slots__ = ("header", "ros2_header", "state", "success")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    state: _entity_state_pb2.EntityState
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., state: _Optional[_Union[_entity_state_pb2.EntityState, _Mapping]] = ..., success: bool = ...) -> None: ...
