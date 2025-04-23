from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.nav_msgs.msg import occupancy_grid_pb2 as _occupancy_grid_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProjectedMap(_message.Message):
    __slots__ = ("header", "map", "min_z", "max_z")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MAP_FIELD_NUMBER: _ClassVar[int]
    MIN_Z_FIELD_NUMBER: _ClassVar[int]
    MAX_Z_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    map: _occupancy_grid_pb2.OccupancyGrid
    min_z: float
    max_z: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., map: _Optional[_Union[_occupancy_grid_pb2.OccupancyGrid, _Mapping]] = ..., min_z: _Optional[float] = ..., max_z: _Optional[float] = ...) -> None: ...
