from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.soccer_object_msgs.msg import goalpost_pb2 as _goalpost_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GoalpostArray(_message.Message):
    __slots__ = ("header", "posts")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    POSTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    posts: _containers.RepeatedCompositeFieldContainer[_goalpost_pb2.Goalpost]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., posts: _Optional[_Iterable[_Union[_goalpost_pb2.Goalpost, _Mapping]]] = ...) -> None: ...
