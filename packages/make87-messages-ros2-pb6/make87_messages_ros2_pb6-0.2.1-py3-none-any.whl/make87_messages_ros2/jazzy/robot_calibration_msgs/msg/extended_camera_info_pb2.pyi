from make87_messages_ros2.jazzy.robot_calibration_msgs.msg import camera_parameter_pb2 as _camera_parameter_pb2
from make87_messages_ros2.jazzy.sensor_msgs.msg import camera_info_pb2 as _camera_info_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ExtendedCameraInfo(_message.Message):
    __slots__ = ("camera_info", "parameters")
    CAMERA_INFO_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    camera_info: _camera_info_pb2.CameraInfo
    parameters: _containers.RepeatedCompositeFieldContainer[_camera_parameter_pb2.CameraParameter]
    def __init__(self, camera_info: _Optional[_Union[_camera_info_pb2.CameraInfo, _Mapping]] = ..., parameters: _Optional[_Iterable[_Union[_camera_parameter_pb2.CameraParameter, _Mapping]]] = ...) -> None: ...
