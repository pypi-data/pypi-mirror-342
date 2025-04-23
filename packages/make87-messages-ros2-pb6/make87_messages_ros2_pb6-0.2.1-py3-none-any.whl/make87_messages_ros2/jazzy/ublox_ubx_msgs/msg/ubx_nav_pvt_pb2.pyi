from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.jazzy.ublox_ubx_msgs.msg import carr_soln_pb2 as _carr_soln_pb2
from make87_messages_ros2.jazzy.ublox_ubx_msgs.msg import gps_fix_pb2 as _gps_fix_pb2
from make87_messages_ros2.jazzy.ublox_ubx_msgs.msg import psmpvt_pb2 as _psmpvt_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UBXNavPVT(_message.Message):
    __slots__ = ("header", "itow", "year", "month", "day", "hour", "min", "sec", "valid_date", "valid_time", "fully_resolved", "valid_mag", "t_acc", "nano", "gps_fix", "gnss_fix_ok", "diff_soln", "psm", "head_veh_valid", "carr_soln", "confirmed_avail", "confirmed_date", "confirmed_time", "num_sv", "lon", "lat", "height", "hmsl", "h_acc", "v_acc", "vel_n", "vel_e", "vel_d", "g_speed", "head_mot", "s_acc", "head_acc", "p_dop", "invalid_llh", "head_veh", "mag_dec", "mag_acc")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ITOW_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    MONTH_FIELD_NUMBER: _ClassVar[int]
    DAY_FIELD_NUMBER: _ClassVar[int]
    HOUR_FIELD_NUMBER: _ClassVar[int]
    MIN_FIELD_NUMBER: _ClassVar[int]
    SEC_FIELD_NUMBER: _ClassVar[int]
    VALID_DATE_FIELD_NUMBER: _ClassVar[int]
    VALID_TIME_FIELD_NUMBER: _ClassVar[int]
    FULLY_RESOLVED_FIELD_NUMBER: _ClassVar[int]
    VALID_MAG_FIELD_NUMBER: _ClassVar[int]
    T_ACC_FIELD_NUMBER: _ClassVar[int]
    NANO_FIELD_NUMBER: _ClassVar[int]
    GPS_FIX_FIELD_NUMBER: _ClassVar[int]
    GNSS_FIX_OK_FIELD_NUMBER: _ClassVar[int]
    DIFF_SOLN_FIELD_NUMBER: _ClassVar[int]
    PSM_FIELD_NUMBER: _ClassVar[int]
    HEAD_VEH_VALID_FIELD_NUMBER: _ClassVar[int]
    CARR_SOLN_FIELD_NUMBER: _ClassVar[int]
    CONFIRMED_AVAIL_FIELD_NUMBER: _ClassVar[int]
    CONFIRMED_DATE_FIELD_NUMBER: _ClassVar[int]
    CONFIRMED_TIME_FIELD_NUMBER: _ClassVar[int]
    NUM_SV_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    HMSL_FIELD_NUMBER: _ClassVar[int]
    H_ACC_FIELD_NUMBER: _ClassVar[int]
    V_ACC_FIELD_NUMBER: _ClassVar[int]
    VEL_N_FIELD_NUMBER: _ClassVar[int]
    VEL_E_FIELD_NUMBER: _ClassVar[int]
    VEL_D_FIELD_NUMBER: _ClassVar[int]
    G_SPEED_FIELD_NUMBER: _ClassVar[int]
    HEAD_MOT_FIELD_NUMBER: _ClassVar[int]
    S_ACC_FIELD_NUMBER: _ClassVar[int]
    HEAD_ACC_FIELD_NUMBER: _ClassVar[int]
    P_DOP_FIELD_NUMBER: _ClassVar[int]
    INVALID_LLH_FIELD_NUMBER: _ClassVar[int]
    HEAD_VEH_FIELD_NUMBER: _ClassVar[int]
    MAG_DEC_FIELD_NUMBER: _ClassVar[int]
    MAG_ACC_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    itow: int
    year: int
    month: int
    day: int
    hour: int
    min: int
    sec: int
    valid_date: bool
    valid_time: bool
    fully_resolved: bool
    valid_mag: bool
    t_acc: int
    nano: int
    gps_fix: _gps_fix_pb2.GpsFix
    gnss_fix_ok: bool
    diff_soln: bool
    psm: _psmpvt_pb2.PSMPVT
    head_veh_valid: bool
    carr_soln: _carr_soln_pb2.CarrSoln
    confirmed_avail: bool
    confirmed_date: bool
    confirmed_time: bool
    num_sv: int
    lon: int
    lat: int
    height: int
    hmsl: int
    h_acc: int
    v_acc: int
    vel_n: int
    vel_e: int
    vel_d: int
    g_speed: int
    head_mot: int
    s_acc: int
    head_acc: int
    p_dop: int
    invalid_llh: bool
    head_veh: int
    mag_dec: int
    mag_acc: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., itow: _Optional[int] = ..., year: _Optional[int] = ..., month: _Optional[int] = ..., day: _Optional[int] = ..., hour: _Optional[int] = ..., min: _Optional[int] = ..., sec: _Optional[int] = ..., valid_date: bool = ..., valid_time: bool = ..., fully_resolved: bool = ..., valid_mag: bool = ..., t_acc: _Optional[int] = ..., nano: _Optional[int] = ..., gps_fix: _Optional[_Union[_gps_fix_pb2.GpsFix, _Mapping]] = ..., gnss_fix_ok: bool = ..., diff_soln: bool = ..., psm: _Optional[_Union[_psmpvt_pb2.PSMPVT, _Mapping]] = ..., head_veh_valid: bool = ..., carr_soln: _Optional[_Union[_carr_soln_pb2.CarrSoln, _Mapping]] = ..., confirmed_avail: bool = ..., confirmed_date: bool = ..., confirmed_time: bool = ..., num_sv: _Optional[int] = ..., lon: _Optional[int] = ..., lat: _Optional[int] = ..., height: _Optional[int] = ..., hmsl: _Optional[int] = ..., h_acc: _Optional[int] = ..., v_acc: _Optional[int] = ..., vel_n: _Optional[int] = ..., vel_e: _Optional[int] = ..., vel_d: _Optional[int] = ..., g_speed: _Optional[int] = ..., head_mot: _Optional[int] = ..., s_acc: _Optional[int] = ..., head_acc: _Optional[int] = ..., p_dop: _Optional[int] = ..., invalid_llh: bool = ..., head_veh: _Optional[int] = ..., mag_dec: _Optional[int] = ..., mag_acc: _Optional[int] = ...) -> None: ...
