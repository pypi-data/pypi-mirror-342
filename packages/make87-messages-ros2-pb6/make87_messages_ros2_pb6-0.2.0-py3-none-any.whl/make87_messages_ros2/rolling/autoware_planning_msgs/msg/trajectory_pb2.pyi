from make87_messages_ros2.rolling.autoware_planning_msgs.msg import trajectory_point_pb2 as _trajectory_point_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Trajectory(_message.Message):
    __slots__ = ("header", "points")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    points: _containers.RepeatedCompositeFieldContainer[_trajectory_point_pb2.TrajectoryPoint]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., points: _Optional[_Iterable[_Union[_trajectory_point_pb2.TrajectoryPoint, _Mapping]]] = ...) -> None: ...
