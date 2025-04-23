from make87_messages_ros2.jazzy.mavros_msgs.msg import waypoint_pb2 as _waypoint_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WaypointList(_message.Message):
    __slots__ = ("current_seq", "waypoints")
    CURRENT_SEQ_FIELD_NUMBER: _ClassVar[int]
    WAYPOINTS_FIELD_NUMBER: _ClassVar[int]
    current_seq: int
    waypoints: _containers.RepeatedCompositeFieldContainer[_waypoint_pb2.Waypoint]
    def __init__(self, current_seq: _Optional[int] = ..., waypoints: _Optional[_Iterable[_Union[_waypoint_pb2.Waypoint, _Mapping]]] = ...) -> None: ...
