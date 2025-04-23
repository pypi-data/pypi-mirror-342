from make87_messages_ros2.jazzy.rcss3d_agent_msgs.msg import spherical_pb2 as _spherical_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Flag(_message.Message):
    __slots__ = ("name", "base")
    NAME_FIELD_NUMBER: _ClassVar[int]
    BASE_FIELD_NUMBER: _ClassVar[int]
    name: str
    base: _spherical_pb2.Spherical
    def __init__(self, name: _Optional[str] = ..., base: _Optional[_Union[_spherical_pb2.Spherical, _Mapping]] = ...) -> None: ...
