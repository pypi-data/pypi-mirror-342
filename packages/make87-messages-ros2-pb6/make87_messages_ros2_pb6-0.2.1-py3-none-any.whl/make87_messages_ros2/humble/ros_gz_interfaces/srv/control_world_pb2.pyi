from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.ros_gz_interfaces.msg import world_control_pb2 as _world_control_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ControlWorldRequest(_message.Message):
    __slots__ = ("header", "world_control")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    WORLD_CONTROL_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    world_control: _world_control_pb2.WorldControl
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., world_control: _Optional[_Union[_world_control_pb2.WorldControl, _Mapping]] = ...) -> None: ...

class ControlWorldResponse(_message.Message):
    __slots__ = ("header", "success")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ...) -> None: ...
