from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MrrHeaderAlignmentState(_message.Message):
    __slots__ = ("header", "can_auto_align_hangle_qf", "can_alignment_status", "can_alignment_state", "can_auto_align_hangle_ref", "can_auto_align_hangle")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CAN_AUTO_ALIGN_HANGLE_QF_FIELD_NUMBER: _ClassVar[int]
    CAN_ALIGNMENT_STATUS_FIELD_NUMBER: _ClassVar[int]
    CAN_ALIGNMENT_STATE_FIELD_NUMBER: _ClassVar[int]
    CAN_AUTO_ALIGN_HANGLE_REF_FIELD_NUMBER: _ClassVar[int]
    CAN_AUTO_ALIGN_HANGLE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    can_auto_align_hangle_qf: int
    can_alignment_status: int
    can_alignment_state: int
    can_auto_align_hangle_ref: float
    can_auto_align_hangle: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., can_auto_align_hangle_qf: _Optional[int] = ..., can_alignment_status: _Optional[int] = ..., can_alignment_state: _Optional[int] = ..., can_auto_align_hangle_ref: _Optional[float] = ..., can_auto_align_hangle: _Optional[float] = ...) -> None: ...
