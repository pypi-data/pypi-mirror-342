from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetStateRequest(_message.Message):
    __slots__ = ("time_stamp", "frame_id")
    TIME_STAMP_FIELD_NUMBER: _ClassVar[int]
    FRAME_ID_FIELD_NUMBER: _ClassVar[int]
    time_stamp: _time_pb2.Time
    frame_id: str
    def __init__(self, time_stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., frame_id: _Optional[str] = ...) -> None: ...

class GetStateResponse(_message.Message):
    __slots__ = ("state", "covariance")
    STATE_FIELD_NUMBER: _ClassVar[int]
    COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    state: _containers.RepeatedScalarFieldContainer[float]
    covariance: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, state: _Optional[_Iterable[float]] = ..., covariance: _Optional[_Iterable[float]] = ...) -> None: ...
