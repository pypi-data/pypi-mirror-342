from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import point_cloud2_pb2 as _point_cloud2_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RoomKeyframe(_message.Message):
    __slots__ = ("header", "ros2_header", "id", "pointcloud", "pose", "keyframes_ids", "planes_ids")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    POINTCLOUD_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    KEYFRAMES_IDS_FIELD_NUMBER: _ClassVar[int]
    PLANES_IDS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    id: int
    pointcloud: _point_cloud2_pb2.PointCloud2
    pose: _pose_pb2.Pose
    keyframes_ids: _containers.RepeatedScalarFieldContainer[int]
    planes_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., id: _Optional[int] = ..., pointcloud: _Optional[_Union[_point_cloud2_pb2.PointCloud2, _Mapping]] = ..., pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., keyframes_ids: _Optional[_Iterable[int]] = ..., planes_ids: _Optional[_Iterable[int]] = ...) -> None: ...
