from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UBXNavHPPosECEF(_message.Message):
    __slots__ = ("header", "version", "itow", "ecef_x", "ecef_y", "ecef_z", "ecef_x_hp", "ecef_y_hp", "ecef_z_hp", "invalid_ecef_x", "invalid_ecef_y", "invalid_ecef_z", "invalid_ecef_x_hp", "invalid_ecef_y_hp", "invalid_ecef_z_hp", "p_acc")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    ITOW_FIELD_NUMBER: _ClassVar[int]
    ECEF_X_FIELD_NUMBER: _ClassVar[int]
    ECEF_Y_FIELD_NUMBER: _ClassVar[int]
    ECEF_Z_FIELD_NUMBER: _ClassVar[int]
    ECEF_X_HP_FIELD_NUMBER: _ClassVar[int]
    ECEF_Y_HP_FIELD_NUMBER: _ClassVar[int]
    ECEF_Z_HP_FIELD_NUMBER: _ClassVar[int]
    INVALID_ECEF_X_FIELD_NUMBER: _ClassVar[int]
    INVALID_ECEF_Y_FIELD_NUMBER: _ClassVar[int]
    INVALID_ECEF_Z_FIELD_NUMBER: _ClassVar[int]
    INVALID_ECEF_X_HP_FIELD_NUMBER: _ClassVar[int]
    INVALID_ECEF_Y_HP_FIELD_NUMBER: _ClassVar[int]
    INVALID_ECEF_Z_HP_FIELD_NUMBER: _ClassVar[int]
    P_ACC_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    version: int
    itow: int
    ecef_x: int
    ecef_y: int
    ecef_z: int
    ecef_x_hp: int
    ecef_y_hp: int
    ecef_z_hp: int
    invalid_ecef_x: bool
    invalid_ecef_y: bool
    invalid_ecef_z: bool
    invalid_ecef_x_hp: bool
    invalid_ecef_y_hp: bool
    invalid_ecef_z_hp: bool
    p_acc: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., version: _Optional[int] = ..., itow: _Optional[int] = ..., ecef_x: _Optional[int] = ..., ecef_y: _Optional[int] = ..., ecef_z: _Optional[int] = ..., ecef_x_hp: _Optional[int] = ..., ecef_y_hp: _Optional[int] = ..., ecef_z_hp: _Optional[int] = ..., invalid_ecef_x: bool = ..., invalid_ecef_y: bool = ..., invalid_ecef_z: bool = ..., invalid_ecef_x_hp: bool = ..., invalid_ecef_y_hp: bool = ..., invalid_ecef_z_hp: bool = ..., p_acc: _Optional[int] = ...) -> None: ...
