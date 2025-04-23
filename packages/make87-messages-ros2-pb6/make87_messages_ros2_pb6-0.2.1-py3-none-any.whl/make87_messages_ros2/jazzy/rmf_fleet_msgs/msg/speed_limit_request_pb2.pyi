from make87_messages_ros2.jazzy.rmf_fleet_msgs.msg import speed_limited_lane_pb2 as _speed_limited_lane_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SpeedLimitRequest(_message.Message):
    __slots__ = ("fleet_name", "speed_limits", "remove_limits")
    FLEET_NAME_FIELD_NUMBER: _ClassVar[int]
    SPEED_LIMITS_FIELD_NUMBER: _ClassVar[int]
    REMOVE_LIMITS_FIELD_NUMBER: _ClassVar[int]
    fleet_name: str
    speed_limits: _containers.RepeatedCompositeFieldContainer[_speed_limited_lane_pb2.SpeedLimitedLane]
    remove_limits: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, fleet_name: _Optional[str] = ..., speed_limits: _Optional[_Iterable[_Union[_speed_limited_lane_pb2.SpeedLimitedLane, _Mapping]]] = ..., remove_limits: _Optional[_Iterable[int]] = ...) -> None: ...
