from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.jazzy.ublox_ubx_msgs.msg import esf_meas_data_item_pb2 as _esf_meas_data_item_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UBXEsfMeas(_message.Message):
    __slots__ = ("header", "time_tag", "time_mark_sent", "time_mark_edge", "calib_ttag_valid", "num_meas", "id", "data", "calib_ttag")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TIME_TAG_FIELD_NUMBER: _ClassVar[int]
    TIME_MARK_SENT_FIELD_NUMBER: _ClassVar[int]
    TIME_MARK_EDGE_FIELD_NUMBER: _ClassVar[int]
    CALIB_TTAG_VALID_FIELD_NUMBER: _ClassVar[int]
    NUM_MEAS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    CALIB_TTAG_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    time_tag: int
    time_mark_sent: int
    time_mark_edge: bool
    calib_ttag_valid: bool
    num_meas: int
    id: int
    data: _containers.RepeatedCompositeFieldContainer[_esf_meas_data_item_pb2.ESFMeasDataItem]
    calib_ttag: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., time_tag: _Optional[int] = ..., time_mark_sent: _Optional[int] = ..., time_mark_edge: bool = ..., calib_ttag_valid: bool = ..., num_meas: _Optional[int] = ..., id: _Optional[int] = ..., data: _Optional[_Iterable[_Union[_esf_meas_data_item_pb2.ESFMeasDataItem, _Mapping]]] = ..., calib_ttag: _Optional[int] = ...) -> None: ...
