from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from make87_messages_ros2.humble.ublox_ubx_msgs.msg import sig_log_event_pb2 as _sig_log_event_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UBXSecSigLog(_message.Message):
    __slots__ = ("header", "ros2_header", "version", "num_events", "events")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    NUM_EVENTS_FIELD_NUMBER: _ClassVar[int]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    version: int
    num_events: int
    events: _containers.RepeatedCompositeFieldContainer[_sig_log_event_pb2.SigLogEvent]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., version: _Optional[int] = ..., num_events: _Optional[int] = ..., events: _Optional[_Iterable[_Union[_sig_log_event_pb2.SigLogEvent, _Mapping]]] = ...) -> None: ...
