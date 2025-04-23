from make87_messages_ros2.jazzy.ublox_msgs.msg import rxm_svsisv_pb2 as _rxm_svsisv_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RxmSVSI(_message.Message):
    __slots__ = ("i_tow", "week", "num_vis", "num_sv", "sv")
    I_TOW_FIELD_NUMBER: _ClassVar[int]
    WEEK_FIELD_NUMBER: _ClassVar[int]
    NUM_VIS_FIELD_NUMBER: _ClassVar[int]
    NUM_SV_FIELD_NUMBER: _ClassVar[int]
    SV_FIELD_NUMBER: _ClassVar[int]
    i_tow: int
    week: int
    num_vis: int
    num_sv: int
    sv: _containers.RepeatedCompositeFieldContainer[_rxm_svsisv_pb2.RxmSVSISV]
    def __init__(self, i_tow: _Optional[int] = ..., week: _Optional[int] = ..., num_vis: _Optional[int] = ..., num_sv: _Optional[int] = ..., sv: _Optional[_Iterable[_Union[_rxm_svsisv_pb2.RxmSVSISV, _Mapping]]] = ...) -> None: ...
