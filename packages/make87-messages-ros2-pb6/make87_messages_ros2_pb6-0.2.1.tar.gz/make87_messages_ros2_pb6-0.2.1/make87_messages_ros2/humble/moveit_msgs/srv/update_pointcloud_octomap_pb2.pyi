from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import point_cloud2_pb2 as _point_cloud2_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UpdatePointcloudOctomapRequest(_message.Message):
    __slots__ = ("header", "cloud")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CLOUD_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    cloud: _point_cloud2_pb2.PointCloud2
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., cloud: _Optional[_Union[_point_cloud2_pb2.PointCloud2, _Mapping]] = ...) -> None: ...

class UpdatePointcloudOctomapResponse(_message.Message):
    __slots__ = ("header", "success")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ...) -> None: ...
