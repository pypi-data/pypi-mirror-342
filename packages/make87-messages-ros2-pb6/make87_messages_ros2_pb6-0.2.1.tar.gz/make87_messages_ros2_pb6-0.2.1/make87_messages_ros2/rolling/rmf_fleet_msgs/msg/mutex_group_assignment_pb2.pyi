from make87_messages_ros2.rolling.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MutexGroupAssignment(_message.Message):
    __slots__ = ("group", "claimant", "claim_time")
    GROUP_FIELD_NUMBER: _ClassVar[int]
    CLAIMANT_FIELD_NUMBER: _ClassVar[int]
    CLAIM_TIME_FIELD_NUMBER: _ClassVar[int]
    group: str
    claimant: int
    claim_time: _time_pb2.Time
    def __init__(self, group: _Optional[str] = ..., claimant: _Optional[int] = ..., claim_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ...) -> None: ...
