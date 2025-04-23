from make87_messages_ros2.rolling.builtin_interfaces.msg import duration_pb2 as _duration_pb2
from make87_messages_ros2.rolling.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.rolling.sensor_msgs.msg import image_pb2 as _image_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TexturedMarker(_message.Message):
    __slots__ = ("header", "ns", "id", "action", "lifetime", "image", "pose", "resolution", "alpha")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    LIFETIME_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    ALPHA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ns: str
    id: int
    action: int
    lifetime: _duration_pb2.Duration
    image: _image_pb2.Image
    pose: _pose_pb2.Pose
    resolution: float
    alpha: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ns: _Optional[str] = ..., id: _Optional[int] = ..., action: _Optional[int] = ..., lifetime: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., image: _Optional[_Union[_image_pb2.Image, _Mapping]] = ..., pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., resolution: _Optional[float] = ..., alpha: _Optional[float] = ...) -> None: ...
