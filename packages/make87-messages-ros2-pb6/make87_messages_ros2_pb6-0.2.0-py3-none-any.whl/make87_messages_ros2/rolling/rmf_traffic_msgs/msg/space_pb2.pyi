from make87_messages_ros2.rolling.geometry_msgs.msg import pose2_d_pb2 as _pose2_d_pb2
from make87_messages_ros2.rolling.rmf_traffic_msgs.msg import shape_pb2 as _shape_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Space(_message.Message):
    __slots__ = ("shape", "pose")
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    shape: _shape_pb2.Shape
    pose: _pose2_d_pb2.Pose2D
    def __init__(self, shape: _Optional[_Union[_shape_pb2.Shape, _Mapping]] = ..., pose: _Optional[_Union[_pose2_d_pb2.Pose2D, _Mapping]] = ...) -> None: ...
