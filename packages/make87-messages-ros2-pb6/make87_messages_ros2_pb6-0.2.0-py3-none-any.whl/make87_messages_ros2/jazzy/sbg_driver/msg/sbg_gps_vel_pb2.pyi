from make87_messages_ros2.jazzy.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.jazzy.sbg_driver.msg import sbg_gps_vel_status_pb2 as _sbg_gps_vel_status_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SbgGpsVel(_message.Message):
    __slots__ = ("header", "time_stamp", "status", "gps_tow", "velocity", "velocity_accuracy", "course", "course_acc")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TIME_STAMP_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    GPS_TOW_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_ACCURACY_FIELD_NUMBER: _ClassVar[int]
    COURSE_FIELD_NUMBER: _ClassVar[int]
    COURSE_ACC_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    time_stamp: int
    status: _sbg_gps_vel_status_pb2.SbgGpsVelStatus
    gps_tow: int
    velocity: _vector3_pb2.Vector3
    velocity_accuracy: _vector3_pb2.Vector3
    course: float
    course_acc: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., time_stamp: _Optional[int] = ..., status: _Optional[_Union[_sbg_gps_vel_status_pb2.SbgGpsVelStatus, _Mapping]] = ..., gps_tow: _Optional[int] = ..., velocity: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., velocity_accuracy: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., course: _Optional[float] = ..., course_acc: _Optional[float] = ...) -> None: ...
