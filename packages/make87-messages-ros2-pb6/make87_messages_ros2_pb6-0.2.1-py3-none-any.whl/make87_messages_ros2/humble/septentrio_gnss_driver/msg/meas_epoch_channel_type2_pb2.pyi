from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MeasEpochChannelType2(_message.Message):
    __slots__ = ("header", "type", "lock_time", "cn0", "offsets_msb", "carrier_msb", "obs_info", "code_offset_lsb", "carrier_lsb", "doppler_offset_lsb")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    LOCK_TIME_FIELD_NUMBER: _ClassVar[int]
    CN0_FIELD_NUMBER: _ClassVar[int]
    OFFSETS_MSB_FIELD_NUMBER: _ClassVar[int]
    CARRIER_MSB_FIELD_NUMBER: _ClassVar[int]
    OBS_INFO_FIELD_NUMBER: _ClassVar[int]
    CODE_OFFSET_LSB_FIELD_NUMBER: _ClassVar[int]
    CARRIER_LSB_FIELD_NUMBER: _ClassVar[int]
    DOPPLER_OFFSET_LSB_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    type: int
    lock_time: int
    cn0: int
    offsets_msb: int
    carrier_msb: int
    obs_info: int
    code_offset_lsb: int
    carrier_lsb: int
    doppler_offset_lsb: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., type: _Optional[int] = ..., lock_time: _Optional[int] = ..., cn0: _Optional[int] = ..., offsets_msb: _Optional[int] = ..., carrier_msb: _Optional[int] = ..., obs_info: _Optional[int] = ..., code_offset_lsb: _Optional[int] = ..., carrier_lsb: _Optional[int] = ..., doppler_offset_lsb: _Optional[int] = ...) -> None: ...
