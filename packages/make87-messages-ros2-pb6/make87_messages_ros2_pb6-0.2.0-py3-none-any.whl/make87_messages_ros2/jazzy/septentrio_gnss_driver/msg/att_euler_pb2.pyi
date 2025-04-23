from make87_messages_ros2.jazzy.septentrio_gnss_driver.msg import block_header_pb2 as _block_header_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AttEuler(_message.Message):
    __slots__ = ("header", "block_header", "nr_sv", "error", "mode", "heading", "pitch", "roll", "pitch_dot", "roll_dot", "heading_dot")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BLOCK_HEADER_FIELD_NUMBER: _ClassVar[int]
    NR_SV_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    HEADING_FIELD_NUMBER: _ClassVar[int]
    PITCH_FIELD_NUMBER: _ClassVar[int]
    ROLL_FIELD_NUMBER: _ClassVar[int]
    PITCH_DOT_FIELD_NUMBER: _ClassVar[int]
    ROLL_DOT_FIELD_NUMBER: _ClassVar[int]
    HEADING_DOT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    block_header: _block_header_pb2.BlockHeader
    nr_sv: int
    error: int
    mode: int
    heading: float
    pitch: float
    roll: float
    pitch_dot: float
    roll_dot: float
    heading_dot: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., block_header: _Optional[_Union[_block_header_pb2.BlockHeader, _Mapping]] = ..., nr_sv: _Optional[int] = ..., error: _Optional[int] = ..., mode: _Optional[int] = ..., heading: _Optional[float] = ..., pitch: _Optional[float] = ..., roll: _Optional[float] = ..., pitch_dot: _Optional[float] = ..., roll_dot: _Optional[float] = ..., heading_dot: _Optional[float] = ...) -> None: ...
