from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_stamped_pb2 as _pose_stamped_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SuctionGrasp(_message.Message):
    __slots__ = ("header", "uuid", "item_uuid", "pose", "quality", "max_suction_surface_length", "max_suction_surface_width")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    ITEM_UUID_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    QUALITY_FIELD_NUMBER: _ClassVar[int]
    MAX_SUCTION_SURFACE_LENGTH_FIELD_NUMBER: _ClassVar[int]
    MAX_SUCTION_SURFACE_WIDTH_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    uuid: str
    item_uuid: str
    pose: _pose_stamped_pb2.PoseStamped
    quality: float
    max_suction_surface_length: float
    max_suction_surface_width: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., uuid: _Optional[str] = ..., item_uuid: _Optional[str] = ..., pose: _Optional[_Union[_pose_stamped_pb2.PoseStamped, _Mapping]] = ..., quality: _Optional[float] = ..., max_suction_surface_length: _Optional[float] = ..., max_suction_surface_width: _Optional[float] = ...) -> None: ...
