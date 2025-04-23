from make87_messages_ros2.jazzy.septentrio_gnss_driver.msg import meas_epoch_channel_type2_pb2 as _meas_epoch_channel_type2_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MeasEpochChannelType1(_message.Message):
    __slots__ = ("rx_channel", "type", "sv_id", "misc", "code_lsb", "doppler", "carrier_lsb", "carrier_msb", "cn0", "lock_time", "obs_info", "n2", "type2")
    RX_CHANNEL_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SV_ID_FIELD_NUMBER: _ClassVar[int]
    MISC_FIELD_NUMBER: _ClassVar[int]
    CODE_LSB_FIELD_NUMBER: _ClassVar[int]
    DOPPLER_FIELD_NUMBER: _ClassVar[int]
    CARRIER_LSB_FIELD_NUMBER: _ClassVar[int]
    CARRIER_MSB_FIELD_NUMBER: _ClassVar[int]
    CN0_FIELD_NUMBER: _ClassVar[int]
    LOCK_TIME_FIELD_NUMBER: _ClassVar[int]
    OBS_INFO_FIELD_NUMBER: _ClassVar[int]
    N2_FIELD_NUMBER: _ClassVar[int]
    TYPE2_FIELD_NUMBER: _ClassVar[int]
    rx_channel: int
    type: int
    sv_id: int
    misc: int
    code_lsb: int
    doppler: int
    carrier_lsb: int
    carrier_msb: int
    cn0: int
    lock_time: int
    obs_info: int
    n2: int
    type2: _containers.RepeatedCompositeFieldContainer[_meas_epoch_channel_type2_pb2.MeasEpochChannelType2]
    def __init__(self, rx_channel: _Optional[int] = ..., type: _Optional[int] = ..., sv_id: _Optional[int] = ..., misc: _Optional[int] = ..., code_lsb: _Optional[int] = ..., doppler: _Optional[int] = ..., carrier_lsb: _Optional[int] = ..., carrier_msb: _Optional[int] = ..., cn0: _Optional[int] = ..., lock_time: _Optional[int] = ..., obs_info: _Optional[int] = ..., n2: _Optional[int] = ..., type2: _Optional[_Iterable[_Union[_meas_epoch_channel_type2_pb2.MeasEpochChannelType2, _Mapping]]] = ...) -> None: ...
