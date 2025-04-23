from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EsrStatus9(_message.Message):
    __slots__ = ("header", "canmsg", "avg_pwr_cwblkg", "sideslip_angle", "serial_num_3rd_byte", "water_spray_target_id", "filtered_xohp_acc_cipv", "path_id_acc_2", "path_id_acc_3")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CANMSG_FIELD_NUMBER: _ClassVar[int]
    AVG_PWR_CWBLKG_FIELD_NUMBER: _ClassVar[int]
    SIDESLIP_ANGLE_FIELD_NUMBER: _ClassVar[int]
    SERIAL_NUM_3RD_BYTE_FIELD_NUMBER: _ClassVar[int]
    WATER_SPRAY_TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    FILTERED_XOHP_ACC_CIPV_FIELD_NUMBER: _ClassVar[int]
    PATH_ID_ACC_2_FIELD_NUMBER: _ClassVar[int]
    PATH_ID_ACC_3_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    canmsg: str
    avg_pwr_cwblkg: int
    sideslip_angle: float
    serial_num_3rd_byte: int
    water_spray_target_id: int
    filtered_xohp_acc_cipv: float
    path_id_acc_2: int
    path_id_acc_3: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., canmsg: _Optional[str] = ..., avg_pwr_cwblkg: _Optional[int] = ..., sideslip_angle: _Optional[float] = ..., serial_num_3rd_byte: _Optional[int] = ..., water_spray_target_id: _Optional[int] = ..., filtered_xohp_acc_cipv: _Optional[float] = ..., path_id_acc_2: _Optional[int] = ..., path_id_acc_3: _Optional[int] = ...) -> None: ...
