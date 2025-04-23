from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import point_stamped_pb2 as _point_stamped_pb2
from make87_messages_ros2.humble.robot_calibration_msgs.msg import extended_camera_info_pb2 as _extended_camera_info_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import image_pb2 as _image_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import point_cloud2_pb2 as _point_cloud2_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Observation(_message.Message):
    __slots__ = ("header", "sensor_name", "features", "ext_camera_info", "cloud", "image")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SENSOR_NAME_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    EXT_CAMERA_INFO_FIELD_NUMBER: _ClassVar[int]
    CLOUD_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    sensor_name: str
    features: _containers.RepeatedCompositeFieldContainer[_point_stamped_pb2.PointStamped]
    ext_camera_info: _extended_camera_info_pb2.ExtendedCameraInfo
    cloud: _point_cloud2_pb2.PointCloud2
    image: _image_pb2.Image
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., sensor_name: _Optional[str] = ..., features: _Optional[_Iterable[_Union[_point_stamped_pb2.PointStamped, _Mapping]]] = ..., ext_camera_info: _Optional[_Union[_extended_camera_info_pb2.ExtendedCameraInfo, _Mapping]] = ..., cloud: _Optional[_Union[_point_cloud2_pb2.PointCloud2, _Mapping]] = ..., image: _Optional[_Union[_image_pb2.Image, _Mapping]] = ...) -> None: ...
