from make87_messages_ros2.rolling.ublox_ubx_msgs.msg import sat_flags_pb2 as _sat_flags_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SatInfo(_message.Message):
    __slots__ = ("gnss_id", "sv_id", "cno", "elev", "azim", "pr_res", "flags")
    GNSS_ID_FIELD_NUMBER: _ClassVar[int]
    SV_ID_FIELD_NUMBER: _ClassVar[int]
    CNO_FIELD_NUMBER: _ClassVar[int]
    ELEV_FIELD_NUMBER: _ClassVar[int]
    AZIM_FIELD_NUMBER: _ClassVar[int]
    PR_RES_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    gnss_id: int
    sv_id: int
    cno: int
    elev: int
    azim: int
    pr_res: int
    flags: _sat_flags_pb2.SatFlags
    def __init__(self, gnss_id: _Optional[int] = ..., sv_id: _Optional[int] = ..., cno: _Optional[int] = ..., elev: _Optional[int] = ..., azim: _Optional[int] = ..., pr_res: _Optional[int] = ..., flags: _Optional[_Union[_sat_flags_pb2.SatFlags, _Mapping]] = ...) -> None: ...
