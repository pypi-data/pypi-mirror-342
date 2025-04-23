from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.jazzy.smacc2_msgs.msg import smacc_transition_pb2 as _smacc_transition_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SmaccTransitionLogEntry(_message.Message):
    __slots__ = ("timestamp", "transition")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TRANSITION_FIELD_NUMBER: _ClassVar[int]
    timestamp: _time_pb2.Time
    transition: _smacc_transition_pb2.SmaccTransition
    def __init__(self, timestamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., transition: _Optional[_Union[_smacc_transition_pb2.SmaccTransition, _Mapping]] = ...) -> None: ...
