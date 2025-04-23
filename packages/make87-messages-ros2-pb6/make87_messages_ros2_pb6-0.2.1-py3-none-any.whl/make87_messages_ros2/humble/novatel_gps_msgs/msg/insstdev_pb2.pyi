from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.novatel_gps_msgs.msg import novatel_extended_solution_status_pb2 as _novatel_extended_solution_status_pb2
from make87_messages_ros2.humble.novatel_gps_msgs.msg import novatel_message_header_pb2 as _novatel_message_header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Insstdev(_message.Message):
    __slots__ = ("header", "ros2_header", "novatel_msg_header", "latitude_dev", "longitude_dev", "height_dev", "north_velocity_dev", "east_velocity_dev", "up_velocity_dev", "roll_dev", "pitch_dev", "azimuth_dev", "extended_solution_status", "time_since_update")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    NOVATEL_MSG_HEADER_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_DEV_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_DEV_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_DEV_FIELD_NUMBER: _ClassVar[int]
    NORTH_VELOCITY_DEV_FIELD_NUMBER: _ClassVar[int]
    EAST_VELOCITY_DEV_FIELD_NUMBER: _ClassVar[int]
    UP_VELOCITY_DEV_FIELD_NUMBER: _ClassVar[int]
    ROLL_DEV_FIELD_NUMBER: _ClassVar[int]
    PITCH_DEV_FIELD_NUMBER: _ClassVar[int]
    AZIMUTH_DEV_FIELD_NUMBER: _ClassVar[int]
    EXTENDED_SOLUTION_STATUS_FIELD_NUMBER: _ClassVar[int]
    TIME_SINCE_UPDATE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    novatel_msg_header: _novatel_message_header_pb2.NovatelMessageHeader
    latitude_dev: float
    longitude_dev: float
    height_dev: float
    north_velocity_dev: float
    east_velocity_dev: float
    up_velocity_dev: float
    roll_dev: float
    pitch_dev: float
    azimuth_dev: float
    extended_solution_status: _novatel_extended_solution_status_pb2.NovatelExtendedSolutionStatus
    time_since_update: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., novatel_msg_header: _Optional[_Union[_novatel_message_header_pb2.NovatelMessageHeader, _Mapping]] = ..., latitude_dev: _Optional[float] = ..., longitude_dev: _Optional[float] = ..., height_dev: _Optional[float] = ..., north_velocity_dev: _Optional[float] = ..., east_velocity_dev: _Optional[float] = ..., up_velocity_dev: _Optional[float] = ..., roll_dev: _Optional[float] = ..., pitch_dev: _Optional[float] = ..., azimuth_dev: _Optional[float] = ..., extended_solution_status: _Optional[_Union[_novatel_extended_solution_status_pb2.NovatelExtendedSolutionStatus, _Mapping]] = ..., time_since_update: _Optional[int] = ...) -> None: ...
