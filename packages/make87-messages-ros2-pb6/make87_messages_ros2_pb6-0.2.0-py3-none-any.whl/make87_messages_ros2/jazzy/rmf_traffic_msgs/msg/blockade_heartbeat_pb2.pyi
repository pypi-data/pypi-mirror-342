from make87_messages_ros2.jazzy.rmf_traffic_msgs.msg import blockade_status_pb2 as _blockade_status_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BlockadeHeartbeat(_message.Message):
    __slots__ = ("statuses", "has_gridlock")
    STATUSES_FIELD_NUMBER: _ClassVar[int]
    HAS_GRIDLOCK_FIELD_NUMBER: _ClassVar[int]
    statuses: _containers.RepeatedCompositeFieldContainer[_blockade_status_pb2.BlockadeStatus]
    has_gridlock: bool
    def __init__(self, statuses: _Optional[_Iterable[_Union[_blockade_status_pb2.BlockadeStatus, _Mapping]]] = ..., has_gridlock: bool = ...) -> None: ...
