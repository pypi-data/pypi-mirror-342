from make87_messages_ros2.rolling.geometry_msgs.msg import pose_with_covariance_stamped_pb2 as _pose_with_covariance_stamped_pb2
from make87_messages_ros2.rolling.nav_msgs.msg import occupancy_grid_pb2 as _occupancy_grid_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetMapRequest(_message.Message):
    __slots__ = ("map", "initial_pose")
    MAP_FIELD_NUMBER: _ClassVar[int]
    INITIAL_POSE_FIELD_NUMBER: _ClassVar[int]
    map: _occupancy_grid_pb2.OccupancyGrid
    initial_pose: _pose_with_covariance_stamped_pb2.PoseWithCovarianceStamped
    def __init__(self, map: _Optional[_Union[_occupancy_grid_pb2.OccupancyGrid, _Mapping]] = ..., initial_pose: _Optional[_Union[_pose_with_covariance_stamped_pb2.PoseWithCovarianceStamped, _Mapping]] = ...) -> None: ...

class SetMapResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
