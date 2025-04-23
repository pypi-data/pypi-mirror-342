from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_with_covariance_stamped_pb2 as _pose_with_covariance_stamped_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetPoseDeprecatedRequest(_message.Message):
    __slots__ = ("pose",)
    POSE_FIELD_NUMBER: _ClassVar[int]
    pose: _pose_with_covariance_stamped_pb2.PoseWithCovarianceStamped
    def __init__(self, pose: _Optional[_Union[_pose_with_covariance_stamped_pb2.PoseWithCovarianceStamped, _Mapping]] = ...) -> None: ...

class SetPoseDeprecatedResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
