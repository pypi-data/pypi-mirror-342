from make87_messages_ros2.jazzy.ublox_msgs.msg import rxm_rawx_meas_pb2 as _rxm_rawx_meas_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RxmRAWX(_message.Message):
    __slots__ = ("rcv_tow", "week", "leap_s", "num_meas", "rec_stat", "version", "reserved1", "meas")
    RCV_TOW_FIELD_NUMBER: _ClassVar[int]
    WEEK_FIELD_NUMBER: _ClassVar[int]
    LEAP_S_FIELD_NUMBER: _ClassVar[int]
    NUM_MEAS_FIELD_NUMBER: _ClassVar[int]
    REC_STAT_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    MEAS_FIELD_NUMBER: _ClassVar[int]
    rcv_tow: float
    week: int
    leap_s: int
    num_meas: int
    rec_stat: int
    version: int
    reserved1: _containers.RepeatedScalarFieldContainer[int]
    meas: _containers.RepeatedCompositeFieldContainer[_rxm_rawx_meas_pb2.RxmRAWXMeas]
    def __init__(self, rcv_tow: _Optional[float] = ..., week: _Optional[int] = ..., leap_s: _Optional[int] = ..., num_meas: _Optional[int] = ..., rec_stat: _Optional[int] = ..., version: _Optional[int] = ..., reserved1: _Optional[_Iterable[int]] = ..., meas: _Optional[_Iterable[_Union[_rxm_rawx_meas_pb2.RxmRAWXMeas, _Mapping]]] = ...) -> None: ...
