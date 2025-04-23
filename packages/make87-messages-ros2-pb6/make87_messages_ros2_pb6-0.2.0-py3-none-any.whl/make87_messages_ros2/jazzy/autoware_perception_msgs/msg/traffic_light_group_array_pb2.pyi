from make87_messages_ros2.jazzy.autoware_perception_msgs.msg import traffic_light_group_pb2 as _traffic_light_group_pb2
from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TrafficLightGroupArray(_message.Message):
    __slots__ = ("stamp", "traffic_light_groups")
    STAMP_FIELD_NUMBER: _ClassVar[int]
    TRAFFIC_LIGHT_GROUPS_FIELD_NUMBER: _ClassVar[int]
    stamp: _time_pb2.Time
    traffic_light_groups: _containers.RepeatedCompositeFieldContainer[_traffic_light_group_pb2.TrafficLightGroup]
    def __init__(self, stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., traffic_light_groups: _Optional[_Iterable[_Union[_traffic_light_group_pb2.TrafficLightGroup, _Mapping]]] = ...) -> None: ...
