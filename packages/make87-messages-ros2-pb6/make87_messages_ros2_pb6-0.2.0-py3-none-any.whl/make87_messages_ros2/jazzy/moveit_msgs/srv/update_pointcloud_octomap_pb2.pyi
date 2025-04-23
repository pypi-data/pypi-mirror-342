from make87_messages_ros2.jazzy.sensor_msgs.msg import point_cloud2_pb2 as _point_cloud2_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UpdatePointcloudOctomapRequest(_message.Message):
    __slots__ = ("cloud",)
    CLOUD_FIELD_NUMBER: _ClassVar[int]
    cloud: _point_cloud2_pb2.PointCloud2
    def __init__(self, cloud: _Optional[_Union[_point_cloud2_pb2.PointCloud2, _Mapping]] = ...) -> None: ...

class UpdatePointcloudOctomapResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
