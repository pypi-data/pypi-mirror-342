from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from make87_messages_ros2.humble.ublox_ubx_msgs.msg import carr_soln_pb2 as _carr_soln_pb2
from make87_messages_ros2.humble.ublox_ubx_msgs.msg import gps_fix_pb2 as _gps_fix_pb2
from make87_messages_ros2.humble.ublox_ubx_msgs.msg import map_matching_pb2 as _map_matching_pb2
from make87_messages_ros2.humble.ublox_ubx_msgs.msg import psm_status_pb2 as _psm_status_pb2
from make87_messages_ros2.humble.ublox_ubx_msgs.msg import spoof_det_pb2 as _spoof_det_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UBXNavStatus(_message.Message):
    __slots__ = ("header", "ros2_header", "itow", "gps_fix", "gps_fix_ok", "diff_soln", "wkn_set", "tow_set", "diff_corr", "carr_soln_valid", "map_matching", "psm", "spoof_det", "carr_soln", "ttff", "msss")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    ITOW_FIELD_NUMBER: _ClassVar[int]
    GPS_FIX_FIELD_NUMBER: _ClassVar[int]
    GPS_FIX_OK_FIELD_NUMBER: _ClassVar[int]
    DIFF_SOLN_FIELD_NUMBER: _ClassVar[int]
    WKN_SET_FIELD_NUMBER: _ClassVar[int]
    TOW_SET_FIELD_NUMBER: _ClassVar[int]
    DIFF_CORR_FIELD_NUMBER: _ClassVar[int]
    CARR_SOLN_VALID_FIELD_NUMBER: _ClassVar[int]
    MAP_MATCHING_FIELD_NUMBER: _ClassVar[int]
    PSM_FIELD_NUMBER: _ClassVar[int]
    SPOOF_DET_FIELD_NUMBER: _ClassVar[int]
    CARR_SOLN_FIELD_NUMBER: _ClassVar[int]
    TTFF_FIELD_NUMBER: _ClassVar[int]
    MSSS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    itow: int
    gps_fix: _gps_fix_pb2.GpsFix
    gps_fix_ok: bool
    diff_soln: bool
    wkn_set: bool
    tow_set: bool
    diff_corr: bool
    carr_soln_valid: bool
    map_matching: _map_matching_pb2.MapMatching
    psm: _psm_status_pb2.PSMStatus
    spoof_det: _spoof_det_pb2.SpoofDet
    carr_soln: _carr_soln_pb2.CarrSoln
    ttff: int
    msss: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., itow: _Optional[int] = ..., gps_fix: _Optional[_Union[_gps_fix_pb2.GpsFix, _Mapping]] = ..., gps_fix_ok: bool = ..., diff_soln: bool = ..., wkn_set: bool = ..., tow_set: bool = ..., diff_corr: bool = ..., carr_soln_valid: bool = ..., map_matching: _Optional[_Union[_map_matching_pb2.MapMatching, _Mapping]] = ..., psm: _Optional[_Union[_psm_status_pb2.PSMStatus, _Mapping]] = ..., spoof_det: _Optional[_Union[_spoof_det_pb2.SpoofDet, _Mapping]] = ..., carr_soln: _Optional[_Union[_carr_soln_pb2.CarrSoln, _Mapping]] = ..., ttff: _Optional[int] = ..., msss: _Optional[int] = ...) -> None: ...
