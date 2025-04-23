from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import camera_info_pb2 as _camera_info_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import image_pb2 as _image_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RGBD(_message.Message):
    __slots__ = ("header", "ros2_header", "rgb_camera_info", "depth_camera_info", "rgb", "depth")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    RGB_CAMERA_INFO_FIELD_NUMBER: _ClassVar[int]
    DEPTH_CAMERA_INFO_FIELD_NUMBER: _ClassVar[int]
    RGB_FIELD_NUMBER: _ClassVar[int]
    DEPTH_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    rgb_camera_info: _camera_info_pb2.CameraInfo
    depth_camera_info: _camera_info_pb2.CameraInfo
    rgb: _image_pb2.Image
    depth: _image_pb2.Image
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., rgb_camera_info: _Optional[_Union[_camera_info_pb2.CameraInfo, _Mapping]] = ..., depth_camera_info: _Optional[_Union[_camera_info_pb2.CameraInfo, _Mapping]] = ..., rgb: _Optional[_Union[_image_pb2.Image, _Mapping]] = ..., depth: _Optional[_Union[_image_pb2.Image, _Mapping]] = ...) -> None: ...
