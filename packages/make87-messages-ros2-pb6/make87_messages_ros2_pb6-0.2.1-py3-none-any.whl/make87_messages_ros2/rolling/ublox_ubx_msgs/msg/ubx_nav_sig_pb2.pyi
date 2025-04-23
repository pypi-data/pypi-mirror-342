from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.rolling.ublox_ubx_msgs.msg import sig_data_pb2 as _sig_data_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UBXNavSig(_message.Message):
    __slots__ = ("header", "itow", "version", "num_sigs", "reserved_0", "sig_data")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ITOW_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    NUM_SIGS_FIELD_NUMBER: _ClassVar[int]
    RESERVED_0_FIELD_NUMBER: _ClassVar[int]
    SIG_DATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    itow: int
    version: int
    num_sigs: int
    reserved_0: _containers.RepeatedScalarFieldContainer[int]
    sig_data: _containers.RepeatedCompositeFieldContainer[_sig_data_pb2.SigData]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., itow: _Optional[int] = ..., version: _Optional[int] = ..., num_sigs: _Optional[int] = ..., reserved_0: _Optional[_Iterable[int]] = ..., sig_data: _Optional[_Iterable[_Union[_sig_data_pb2.SigData, _Mapping]]] = ...) -> None: ...
