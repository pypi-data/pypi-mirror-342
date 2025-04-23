from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Packet(_message.Message):
    __slots__ = ("header", "ros2_header", "data", "b_o_s", "e_o_s", "granulepos", "packetno")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    B_O_S_FIELD_NUMBER: _ClassVar[int]
    E_O_S_FIELD_NUMBER: _ClassVar[int]
    GRANULEPOS_FIELD_NUMBER: _ClassVar[int]
    PACKETNO_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    data: _containers.RepeatedScalarFieldContainer[int]
    b_o_s: int
    e_o_s: int
    granulepos: int
    packetno: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., data: _Optional[_Iterable[int]] = ..., b_o_s: _Optional[int] = ..., e_o_s: _Optional[int] = ..., granulepos: _Optional[int] = ..., packetno: _Optional[int] = ...) -> None: ...
