from make87_messages_ros2.rolling.geographic_msgs.msg import geo_path_pb2 as _geo_path_pb2
from make87_messages_ros2.rolling.geographic_msgs.msg import geo_point_pb2 as _geo_point_pb2
from make87_messages_ros2.rolling.unique_identifier_msgs.msg import uuid_pb2 as _uuid_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetGeoPathRequest(_message.Message):
    __slots__ = ("start", "goal")
    START_FIELD_NUMBER: _ClassVar[int]
    GOAL_FIELD_NUMBER: _ClassVar[int]
    start: _geo_point_pb2.GeoPoint
    goal: _geo_point_pb2.GeoPoint
    def __init__(self, start: _Optional[_Union[_geo_point_pb2.GeoPoint, _Mapping]] = ..., goal: _Optional[_Union[_geo_point_pb2.GeoPoint, _Mapping]] = ...) -> None: ...

class GetGeoPathResponse(_message.Message):
    __slots__ = ("success", "status", "plan", "network", "start_seg", "goal_seg", "distance")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PLAN_FIELD_NUMBER: _ClassVar[int]
    NETWORK_FIELD_NUMBER: _ClassVar[int]
    START_SEG_FIELD_NUMBER: _ClassVar[int]
    GOAL_SEG_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    status: str
    plan: _geo_path_pb2.GeoPath
    network: _uuid_pb2.UUID
    start_seg: _uuid_pb2.UUID
    goal_seg: _uuid_pb2.UUID
    distance: float
    def __init__(self, success: bool = ..., status: _Optional[str] = ..., plan: _Optional[_Union[_geo_path_pb2.GeoPath, _Mapping]] = ..., network: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., start_seg: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., goal_seg: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., distance: _Optional[float] = ...) -> None: ...
