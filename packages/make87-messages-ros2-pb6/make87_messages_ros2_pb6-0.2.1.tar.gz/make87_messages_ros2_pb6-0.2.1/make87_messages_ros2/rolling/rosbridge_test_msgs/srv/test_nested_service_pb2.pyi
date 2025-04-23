from make87_messages_ros2.rolling.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.rolling.std_msgs.msg import float64_pb2 as _float64_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TestNestedServiceRequest(_message.Message):
    __slots__ = ("pose",)
    POSE_FIELD_NUMBER: _ClassVar[int]
    pose: _pose_pb2.Pose
    def __init__(self, pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ...) -> None: ...

class TestNestedServiceResponse(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _float64_pb2.Float64
    def __init__(self, data: _Optional[_Union[_float64_pb2.Float64, _Mapping]] = ...) -> None: ...
