from make87_messages_ros2.jazzy.ublox_ubx_msgs.msg import sig_flags_pb2 as _sig_flags_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SigData(_message.Message):
    __slots__ = ("gnss_id", "sv_id", "sig_id", "freq_id", "pr_res", "cno", "quality_ind", "corr_source", "iono_model", "sig_flags")
    GNSS_ID_FIELD_NUMBER: _ClassVar[int]
    SV_ID_FIELD_NUMBER: _ClassVar[int]
    SIG_ID_FIELD_NUMBER: _ClassVar[int]
    FREQ_ID_FIELD_NUMBER: _ClassVar[int]
    PR_RES_FIELD_NUMBER: _ClassVar[int]
    CNO_FIELD_NUMBER: _ClassVar[int]
    QUALITY_IND_FIELD_NUMBER: _ClassVar[int]
    CORR_SOURCE_FIELD_NUMBER: _ClassVar[int]
    IONO_MODEL_FIELD_NUMBER: _ClassVar[int]
    SIG_FLAGS_FIELD_NUMBER: _ClassVar[int]
    gnss_id: int
    sv_id: int
    sig_id: int
    freq_id: int
    pr_res: int
    cno: int
    quality_ind: int
    corr_source: int
    iono_model: int
    sig_flags: _sig_flags_pb2.SigFlags
    def __init__(self, gnss_id: _Optional[int] = ..., sv_id: _Optional[int] = ..., sig_id: _Optional[int] = ..., freq_id: _Optional[int] = ..., pr_res: _Optional[int] = ..., cno: _Optional[int] = ..., quality_ind: _Optional[int] = ..., corr_source: _Optional[int] = ..., iono_model: _Optional[int] = ..., sig_flags: _Optional[_Union[_sig_flags_pb2.SigFlags, _Mapping]] = ...) -> None: ...
