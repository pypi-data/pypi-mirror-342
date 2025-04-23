from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_stamped_pb2 as _pose_stamped_pb2
from make87_messages_ros2.humble.shape_msgs.msg import solid_primitive_pb2 as _solid_primitive_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RegionOfInterest3D(_message.Message):
    __slots__ = ("header", "id", "pose", "primitive")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    PRIMITIVE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    id: str
    pose: _pose_stamped_pb2.PoseStamped
    primitive: _solid_primitive_pb2.SolidPrimitive
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., id: _Optional[str] = ..., pose: _Optional[_Union[_pose_stamped_pb2.PoseStamped, _Mapping]] = ..., primitive: _Optional[_Union[_solid_primitive_pb2.SolidPrimitive, _Mapping]] = ...) -> None: ...
