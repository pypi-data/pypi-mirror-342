from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EntityFactory(_message.Message):
    __slots__ = ("header", "name", "allow_renaming", "sdf", "sdf_filename", "clone_name", "pose", "relative_to")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ALLOW_RENAMING_FIELD_NUMBER: _ClassVar[int]
    SDF_FIELD_NUMBER: _ClassVar[int]
    SDF_FILENAME_FIELD_NUMBER: _ClassVar[int]
    CLONE_NAME_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_TO_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    allow_renaming: bool
    sdf: str
    sdf_filename: str
    clone_name: str
    pose: _pose_pb2.Pose
    relative_to: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., allow_renaming: bool = ..., sdf: _Optional[str] = ..., sdf_filename: _Optional[str] = ..., clone_name: _Optional[str] = ..., pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., relative_to: _Optional[str] = ...) -> None: ...
