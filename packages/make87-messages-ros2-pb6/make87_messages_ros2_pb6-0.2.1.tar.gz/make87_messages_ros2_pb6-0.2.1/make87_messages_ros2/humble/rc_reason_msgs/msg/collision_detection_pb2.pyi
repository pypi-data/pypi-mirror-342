from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import point_pb2 as _point_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CollisionDetection(_message.Message):
    __slots__ = ("header", "gripper_id", "pre_grasp_offset")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    GRIPPER_ID_FIELD_NUMBER: _ClassVar[int]
    PRE_GRASP_OFFSET_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    gripper_id: str
    pre_grasp_offset: _point_pb2.Point
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., gripper_id: _Optional[str] = ..., pre_grasp_offset: _Optional[_Union[_point_pb2.Point, _Mapping]] = ...) -> None: ...
