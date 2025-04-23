from make87_messages_ros2.jazzy.geographic_msgs.msg import geo_pose_pb2 as _geo_pose_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GeoPoseWithCovariance(_message.Message):
    __slots__ = ("pose", "covariance")
    POSE_FIELD_NUMBER: _ClassVar[int]
    COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    pose: _geo_pose_pb2.GeoPose
    covariance: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, pose: _Optional[_Union[_geo_pose_pb2.GeoPose, _Mapping]] = ..., covariance: _Optional[_Iterable[float]] = ...) -> None: ...
