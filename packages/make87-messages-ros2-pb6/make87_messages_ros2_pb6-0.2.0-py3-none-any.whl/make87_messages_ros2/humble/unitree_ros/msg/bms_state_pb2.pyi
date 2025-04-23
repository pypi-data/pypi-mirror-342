from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BmsState(_message.Message):
    __slots__ = ("header", "version_h", "version_l", "bms_status", "soc", "current", "cycle", "bq_ntc", "mcu_ntc", "cell_vol")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VERSION_H_FIELD_NUMBER: _ClassVar[int]
    VERSION_L_FIELD_NUMBER: _ClassVar[int]
    BMS_STATUS_FIELD_NUMBER: _ClassVar[int]
    SOC_FIELD_NUMBER: _ClassVar[int]
    CURRENT_FIELD_NUMBER: _ClassVar[int]
    CYCLE_FIELD_NUMBER: _ClassVar[int]
    BQ_NTC_FIELD_NUMBER: _ClassVar[int]
    MCU_NTC_FIELD_NUMBER: _ClassVar[int]
    CELL_VOL_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    version_h: int
    version_l: int
    bms_status: int
    soc: int
    current: int
    cycle: int
    bq_ntc: _containers.RepeatedScalarFieldContainer[int]
    mcu_ntc: _containers.RepeatedScalarFieldContainer[int]
    cell_vol: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., version_h: _Optional[int] = ..., version_l: _Optional[int] = ..., bms_status: _Optional[int] = ..., soc: _Optional[int] = ..., current: _Optional[int] = ..., cycle: _Optional[int] = ..., bq_ntc: _Optional[_Iterable[int]] = ..., mcu_ntc: _Optional[_Iterable[int]] = ..., cell_vol: _Optional[_Iterable[int]] = ...) -> None: ...
