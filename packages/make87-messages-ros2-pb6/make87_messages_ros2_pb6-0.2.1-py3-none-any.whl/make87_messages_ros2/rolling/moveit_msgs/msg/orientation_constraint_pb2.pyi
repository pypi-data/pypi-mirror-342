from make87_messages_ros2.rolling.geometry_msgs.msg import quaternion_pb2 as _quaternion_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OrientationConstraint(_message.Message):
    __slots__ = ("header", "orientation", "link_name", "absolute_x_axis_tolerance", "absolute_y_axis_tolerance", "absolute_z_axis_tolerance", "parameterization", "weight")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    LINK_NAME_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_X_AXIS_TOLERANCE_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_Y_AXIS_TOLERANCE_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_Z_AXIS_TOLERANCE_FIELD_NUMBER: _ClassVar[int]
    PARAMETERIZATION_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    orientation: _quaternion_pb2.Quaternion
    link_name: str
    absolute_x_axis_tolerance: float
    absolute_y_axis_tolerance: float
    absolute_z_axis_tolerance: float
    parameterization: int
    weight: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., orientation: _Optional[_Union[_quaternion_pb2.Quaternion, _Mapping]] = ..., link_name: _Optional[str] = ..., absolute_x_axis_tolerance: _Optional[float] = ..., absolute_y_axis_tolerance: _Optional[float] = ..., absolute_z_axis_tolerance: _Optional[float] = ..., parameterization: _Optional[int] = ..., weight: _Optional[float] = ...) -> None: ...
