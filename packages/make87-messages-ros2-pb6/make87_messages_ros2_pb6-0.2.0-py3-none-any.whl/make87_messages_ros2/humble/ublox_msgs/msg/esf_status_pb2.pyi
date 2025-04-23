from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.ublox_msgs.msg import esf_status_sens_pb2 as _esf_status_sens_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EsfSTATUS(_message.Message):
    __slots__ = ("header", "i_tow", "version", "reserved1", "fusion_mode", "reserved2", "num_sens", "sens")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    I_TOW_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    FUSION_MODE_FIELD_NUMBER: _ClassVar[int]
    RESERVED2_FIELD_NUMBER: _ClassVar[int]
    NUM_SENS_FIELD_NUMBER: _ClassVar[int]
    SENS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    i_tow: int
    version: int
    reserved1: _containers.RepeatedScalarFieldContainer[int]
    fusion_mode: int
    reserved2: _containers.RepeatedScalarFieldContainer[int]
    num_sens: int
    sens: _containers.RepeatedCompositeFieldContainer[_esf_status_sens_pb2.EsfSTATUSSens]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., i_tow: _Optional[int] = ..., version: _Optional[int] = ..., reserved1: _Optional[_Iterable[int]] = ..., fusion_mode: _Optional[int] = ..., reserved2: _Optional[_Iterable[int]] = ..., num_sens: _Optional[int] = ..., sens: _Optional[_Iterable[_Union[_esf_status_sens_pb2.EsfSTATUSSens, _Mapping]]] = ...) -> None: ...
