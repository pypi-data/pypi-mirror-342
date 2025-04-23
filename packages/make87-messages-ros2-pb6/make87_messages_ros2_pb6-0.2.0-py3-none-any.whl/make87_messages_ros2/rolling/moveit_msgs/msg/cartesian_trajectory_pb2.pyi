from make87_messages_ros2.rolling.moveit_msgs.msg import cartesian_trajectory_point_pb2 as _cartesian_trajectory_point_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CartesianTrajectory(_message.Message):
    __slots__ = ("header", "tracked_frame", "points")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TRACKED_FRAME_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    tracked_frame: str
    points: _containers.RepeatedCompositeFieldContainer[_cartesian_trajectory_point_pb2.CartesianTrajectoryPoint]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., tracked_frame: _Optional[str] = ..., points: _Optional[_Iterable[_Union[_cartesian_trajectory_point_pb2.CartesianTrajectoryPoint, _Mapping]]] = ...) -> None: ...
