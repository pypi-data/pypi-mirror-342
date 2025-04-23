from make87_messages_ros2.rolling.geometry_msgs.msg import pose_stamped_pb2 as _pose_stamped_pb2
from make87_messages_ros2.rolling.rc_reason_msgs.msg import rectangle_pb2 as _rectangle_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Item(_message.Message):
    __slots__ = ("uuid", "grasp_uuids", "type", "rectangle", "pose")
    UUID_FIELD_NUMBER: _ClassVar[int]
    GRASP_UUIDS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    RECTANGLE_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    grasp_uuids: _containers.RepeatedScalarFieldContainer[str]
    type: str
    rectangle: _rectangle_pb2.Rectangle
    pose: _pose_stamped_pb2.PoseStamped
    def __init__(self, uuid: _Optional[str] = ..., grasp_uuids: _Optional[_Iterable[str]] = ..., type: _Optional[str] = ..., rectangle: _Optional[_Union[_rectangle_pb2.Rectangle, _Mapping]] = ..., pose: _Optional[_Union[_pose_stamped_pb2.PoseStamped, _Mapping]] = ...) -> None: ...
