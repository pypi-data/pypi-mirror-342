from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.ds_dbw_msgs.msg import ambient_light_pb2 as _ambient_light_pb2
from make87_messages_ros2.humble.ds_dbw_msgs.msg import headlight_ctrl_high_pb2 as _headlight_ctrl_high_pb2
from make87_messages_ros2.humble.ds_dbw_msgs.msg import headlight_ctrl_low_pb2 as _headlight_ctrl_low_pb2
from make87_messages_ros2.humble.ds_dbw_msgs.msg import prk_brk_stat_pb2 as _prk_brk_stat_pb2
from make87_messages_ros2.humble.ds_dbw_msgs.msg import wiper_pb2 as _wiper_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MiscReport(_message.Message):
    __slots__ = ("header", "ros2_header", "parking_brake", "passenger_detect", "passenger_airbag", "buckle_driver", "buckle_passenger", "door_driver", "door_passenger", "door_rear_left", "door_rear_right", "door_hood", "door_trunk", "btn_ld_ok", "btn_ld_up", "btn_ld_down", "btn_ld_left", "btn_ld_right", "btn_rd_ok", "btn_rd_up", "btn_rd_down", "btn_rd_left", "btn_rd_right", "btn_cc_mode", "btn_cc_on", "btn_cc_off", "btn_cc_res", "btn_cc_cncl", "btn_cc_on_off", "btn_cc_res_cncl", "btn_cc_res_inc", "btn_cc_res_dec", "btn_cc_set_inc", "btn_cc_set_dec", "btn_acc_gap_inc", "btn_acc_gap_dec", "btn_limit_on_off", "btn_la_on_off", "btn_apa", "btn_media", "btn_vol_inc", "btn_vol_dec", "btn_mute", "btn_speak", "btn_prev", "btn_next", "btn_call_start", "btn_call_end", "wiper", "headlight_low", "headlight_high", "headlight_low_control", "headlight_high_control", "ambient_light", "outside_air_temp")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    PARKING_BRAKE_FIELD_NUMBER: _ClassVar[int]
    PASSENGER_DETECT_FIELD_NUMBER: _ClassVar[int]
    PASSENGER_AIRBAG_FIELD_NUMBER: _ClassVar[int]
    BUCKLE_DRIVER_FIELD_NUMBER: _ClassVar[int]
    BUCKLE_PASSENGER_FIELD_NUMBER: _ClassVar[int]
    DOOR_DRIVER_FIELD_NUMBER: _ClassVar[int]
    DOOR_PASSENGER_FIELD_NUMBER: _ClassVar[int]
    DOOR_REAR_LEFT_FIELD_NUMBER: _ClassVar[int]
    DOOR_REAR_RIGHT_FIELD_NUMBER: _ClassVar[int]
    DOOR_HOOD_FIELD_NUMBER: _ClassVar[int]
    DOOR_TRUNK_FIELD_NUMBER: _ClassVar[int]
    BTN_LD_OK_FIELD_NUMBER: _ClassVar[int]
    BTN_LD_UP_FIELD_NUMBER: _ClassVar[int]
    BTN_LD_DOWN_FIELD_NUMBER: _ClassVar[int]
    BTN_LD_LEFT_FIELD_NUMBER: _ClassVar[int]
    BTN_LD_RIGHT_FIELD_NUMBER: _ClassVar[int]
    BTN_RD_OK_FIELD_NUMBER: _ClassVar[int]
    BTN_RD_UP_FIELD_NUMBER: _ClassVar[int]
    BTN_RD_DOWN_FIELD_NUMBER: _ClassVar[int]
    BTN_RD_LEFT_FIELD_NUMBER: _ClassVar[int]
    BTN_RD_RIGHT_FIELD_NUMBER: _ClassVar[int]
    BTN_CC_MODE_FIELD_NUMBER: _ClassVar[int]
    BTN_CC_ON_FIELD_NUMBER: _ClassVar[int]
    BTN_CC_OFF_FIELD_NUMBER: _ClassVar[int]
    BTN_CC_RES_FIELD_NUMBER: _ClassVar[int]
    BTN_CC_CNCL_FIELD_NUMBER: _ClassVar[int]
    BTN_CC_ON_OFF_FIELD_NUMBER: _ClassVar[int]
    BTN_CC_RES_CNCL_FIELD_NUMBER: _ClassVar[int]
    BTN_CC_RES_INC_FIELD_NUMBER: _ClassVar[int]
    BTN_CC_RES_DEC_FIELD_NUMBER: _ClassVar[int]
    BTN_CC_SET_INC_FIELD_NUMBER: _ClassVar[int]
    BTN_CC_SET_DEC_FIELD_NUMBER: _ClassVar[int]
    BTN_ACC_GAP_INC_FIELD_NUMBER: _ClassVar[int]
    BTN_ACC_GAP_DEC_FIELD_NUMBER: _ClassVar[int]
    BTN_LIMIT_ON_OFF_FIELD_NUMBER: _ClassVar[int]
    BTN_LA_ON_OFF_FIELD_NUMBER: _ClassVar[int]
    BTN_APA_FIELD_NUMBER: _ClassVar[int]
    BTN_MEDIA_FIELD_NUMBER: _ClassVar[int]
    BTN_VOL_INC_FIELD_NUMBER: _ClassVar[int]
    BTN_VOL_DEC_FIELD_NUMBER: _ClassVar[int]
    BTN_MUTE_FIELD_NUMBER: _ClassVar[int]
    BTN_SPEAK_FIELD_NUMBER: _ClassVar[int]
    BTN_PREV_FIELD_NUMBER: _ClassVar[int]
    BTN_NEXT_FIELD_NUMBER: _ClassVar[int]
    BTN_CALL_START_FIELD_NUMBER: _ClassVar[int]
    BTN_CALL_END_FIELD_NUMBER: _ClassVar[int]
    WIPER_FIELD_NUMBER: _ClassVar[int]
    HEADLIGHT_LOW_FIELD_NUMBER: _ClassVar[int]
    HEADLIGHT_HIGH_FIELD_NUMBER: _ClassVar[int]
    HEADLIGHT_LOW_CONTROL_FIELD_NUMBER: _ClassVar[int]
    HEADLIGHT_HIGH_CONTROL_FIELD_NUMBER: _ClassVar[int]
    AMBIENT_LIGHT_FIELD_NUMBER: _ClassVar[int]
    OUTSIDE_AIR_TEMP_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    parking_brake: _prk_brk_stat_pb2.PrkBrkStat
    passenger_detect: bool
    passenger_airbag: bool
    buckle_driver: bool
    buckle_passenger: bool
    door_driver: bool
    door_passenger: bool
    door_rear_left: bool
    door_rear_right: bool
    door_hood: bool
    door_trunk: bool
    btn_ld_ok: bool
    btn_ld_up: bool
    btn_ld_down: bool
    btn_ld_left: bool
    btn_ld_right: bool
    btn_rd_ok: bool
    btn_rd_up: bool
    btn_rd_down: bool
    btn_rd_left: bool
    btn_rd_right: bool
    btn_cc_mode: bool
    btn_cc_on: bool
    btn_cc_off: bool
    btn_cc_res: bool
    btn_cc_cncl: bool
    btn_cc_on_off: bool
    btn_cc_res_cncl: bool
    btn_cc_res_inc: bool
    btn_cc_res_dec: bool
    btn_cc_set_inc: bool
    btn_cc_set_dec: bool
    btn_acc_gap_inc: bool
    btn_acc_gap_dec: bool
    btn_limit_on_off: bool
    btn_la_on_off: bool
    btn_apa: bool
    btn_media: bool
    btn_vol_inc: bool
    btn_vol_dec: bool
    btn_mute: bool
    btn_speak: bool
    btn_prev: bool
    btn_next: bool
    btn_call_start: bool
    btn_call_end: bool
    wiper: _wiper_pb2.Wiper
    headlight_low: bool
    headlight_high: bool
    headlight_low_control: _headlight_ctrl_low_pb2.HeadlightCtrlLow
    headlight_high_control: _headlight_ctrl_high_pb2.HeadlightCtrlHigh
    ambient_light: _ambient_light_pb2.AmbientLight
    outside_air_temp: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., parking_brake: _Optional[_Union[_prk_brk_stat_pb2.PrkBrkStat, _Mapping]] = ..., passenger_detect: bool = ..., passenger_airbag: bool = ..., buckle_driver: bool = ..., buckle_passenger: bool = ..., door_driver: bool = ..., door_passenger: bool = ..., door_rear_left: bool = ..., door_rear_right: bool = ..., door_hood: bool = ..., door_trunk: bool = ..., btn_ld_ok: bool = ..., btn_ld_up: bool = ..., btn_ld_down: bool = ..., btn_ld_left: bool = ..., btn_ld_right: bool = ..., btn_rd_ok: bool = ..., btn_rd_up: bool = ..., btn_rd_down: bool = ..., btn_rd_left: bool = ..., btn_rd_right: bool = ..., btn_cc_mode: bool = ..., btn_cc_on: bool = ..., btn_cc_off: bool = ..., btn_cc_res: bool = ..., btn_cc_cncl: bool = ..., btn_cc_on_off: bool = ..., btn_cc_res_cncl: bool = ..., btn_cc_res_inc: bool = ..., btn_cc_res_dec: bool = ..., btn_cc_set_inc: bool = ..., btn_cc_set_dec: bool = ..., btn_acc_gap_inc: bool = ..., btn_acc_gap_dec: bool = ..., btn_limit_on_off: bool = ..., btn_la_on_off: bool = ..., btn_apa: bool = ..., btn_media: bool = ..., btn_vol_inc: bool = ..., btn_vol_dec: bool = ..., btn_mute: bool = ..., btn_speak: bool = ..., btn_prev: bool = ..., btn_next: bool = ..., btn_call_start: bool = ..., btn_call_end: bool = ..., wiper: _Optional[_Union[_wiper_pb2.Wiper, _Mapping]] = ..., headlight_low: bool = ..., headlight_high: bool = ..., headlight_low_control: _Optional[_Union[_headlight_ctrl_low_pb2.HeadlightCtrlLow, _Mapping]] = ..., headlight_high_control: _Optional[_Union[_headlight_ctrl_high_pb2.HeadlightCtrlHigh, _Mapping]] = ..., ambient_light: _Optional[_Union[_ambient_light_pb2.AmbientLight, _Mapping]] = ..., outside_air_temp: _Optional[float] = ...) -> None: ...
