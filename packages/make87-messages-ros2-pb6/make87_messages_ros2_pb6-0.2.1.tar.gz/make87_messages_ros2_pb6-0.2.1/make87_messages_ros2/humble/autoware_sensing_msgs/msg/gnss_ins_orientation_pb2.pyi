from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import quaternion_pb2 as _quaternion_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GnssInsOrientation(_message.Message):
    __slots__ = ("header", "orientation", "rmse_rotation_x", "rmse_rotation_y", "rmse_rotation_z")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    RMSE_ROTATION_X_FIELD_NUMBER: _ClassVar[int]
    RMSE_ROTATION_Y_FIELD_NUMBER: _ClassVar[int]
    RMSE_ROTATION_Z_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    orientation: _quaternion_pb2.Quaternion
    rmse_rotation_x: float
    rmse_rotation_y: float
    rmse_rotation_z: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., orientation: _Optional[_Union[_quaternion_pb2.Quaternion, _Mapping]] = ..., rmse_rotation_x: _Optional[float] = ..., rmse_rotation_y: _Optional[float] = ..., rmse_rotation_z: _Optional[float] = ...) -> None: ...
