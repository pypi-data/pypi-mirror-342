from make87_messages_ros2.rolling.rmf_door_msgs.msg import door_sessions_pb2 as _door_sessions_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SupervisorHeartbeat(_message.Message):
    __slots__ = ("all_sessions",)
    ALL_SESSIONS_FIELD_NUMBER: _ClassVar[int]
    all_sessions: _containers.RepeatedCompositeFieldContainer[_door_sessions_pb2.DoorSessions]
    def __init__(self, all_sessions: _Optional[_Iterable[_Union[_door_sessions_pb2.DoorSessions, _Mapping]]] = ...) -> None: ...
