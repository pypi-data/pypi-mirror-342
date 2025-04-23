from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.bosch_locator_bridge.msg import client_expand_map_overwrite_zone_information_pb2 as _client_expand_map_overwrite_zone_information_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_array_pb2 as _pose_array_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClientExpandMapVisualization(_message.Message):
    __slots__ = ("header", "timestamp", "visualization_id", "zones", "prior_map_poses", "prior_map_pose_types")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VISUALIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    ZONES_FIELD_NUMBER: _ClassVar[int]
    PRIOR_MAP_POSES_FIELD_NUMBER: _ClassVar[int]
    PRIOR_MAP_POSE_TYPES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    timestamp: _time_pb2.Time
    visualization_id: int
    zones: _containers.RepeatedCompositeFieldContainer[_client_expand_map_overwrite_zone_information_pb2.ClientExpandMapOverwriteZoneInformation]
    prior_map_poses: _pose_array_pb2.PoseArray
    prior_map_pose_types: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., timestamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., visualization_id: _Optional[int] = ..., zones: _Optional[_Iterable[_Union[_client_expand_map_overwrite_zone_information_pb2.ClientExpandMapOverwriteZoneInformation, _Mapping]]] = ..., prior_map_poses: _Optional[_Union[_pose_array_pb2.PoseArray, _Mapping]] = ..., prior_map_pose_types: _Optional[_Iterable[int]] = ...) -> None: ...
