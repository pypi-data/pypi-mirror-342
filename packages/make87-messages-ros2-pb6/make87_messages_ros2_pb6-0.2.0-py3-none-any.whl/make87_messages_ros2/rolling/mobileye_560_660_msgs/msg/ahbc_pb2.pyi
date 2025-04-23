from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Ahbc(_message.Message):
    __slots__ = ("header", "high_low_beam_decision", "reasons_for_switch_to_low_beam")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    HIGH_LOW_BEAM_DECISION_FIELD_NUMBER: _ClassVar[int]
    REASONS_FOR_SWITCH_TO_LOW_BEAM_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    high_low_beam_decision: int
    reasons_for_switch_to_low_beam: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., high_low_beam_decision: _Optional[int] = ..., reasons_for_switch_to_low_beam: _Optional[int] = ...) -> None: ...
