from make87_messages_ros2.jazzy.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.jazzy.moveit_msgs.msg import bounding_volume_pb2 as _bounding_volume_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PositionConstraint(_message.Message):
    __slots__ = ("header", "link_name", "target_point_offset", "constraint_region", "weight")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LINK_NAME_FIELD_NUMBER: _ClassVar[int]
    TARGET_POINT_OFFSET_FIELD_NUMBER: _ClassVar[int]
    CONSTRAINT_REGION_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    link_name: str
    target_point_offset: _vector3_pb2.Vector3
    constraint_region: _bounding_volume_pb2.BoundingVolume
    weight: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., link_name: _Optional[str] = ..., target_point_offset: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., constraint_region: _Optional[_Union[_bounding_volume_pb2.BoundingVolume, _Mapping]] = ..., weight: _Optional[float] = ...) -> None: ...
