from make87_messages_ros2.jazzy.mavros_msgs.msg import waypoint_pb2 as _waypoint_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WaypointPushRequest(_message.Message):
    __slots__ = ("start_index", "waypoints")
    START_INDEX_FIELD_NUMBER: _ClassVar[int]
    WAYPOINTS_FIELD_NUMBER: _ClassVar[int]
    start_index: int
    waypoints: _containers.RepeatedCompositeFieldContainer[_waypoint_pb2.Waypoint]
    def __init__(self, start_index: _Optional[int] = ..., waypoints: _Optional[_Iterable[_Union[_waypoint_pb2.Waypoint, _Mapping]]] = ...) -> None: ...

class WaypointPushResponse(_message.Message):
    __slots__ = ("success", "wp_transfered")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    WP_TRANSFERED_FIELD_NUMBER: _ClassVar[int]
    success: bool
    wp_transfered: int
    def __init__(self, success: bool = ..., wp_transfered: _Optional[int] = ...) -> None: ...
