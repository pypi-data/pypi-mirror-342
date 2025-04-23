from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MapMetaData(_message.Message):
    __slots__ = ("header", "map_load_time", "resolution", "width", "height", "origin")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MAP_LOAD_TIME_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    map_load_time: _time_pb2.Time
    resolution: float
    width: int
    height: int
    origin: _pose_pb2.Pose
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., map_load_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., resolution: _Optional[float] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., origin: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ...) -> None: ...
