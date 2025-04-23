from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.humble.rc_common_msgs.msg import return_code_pb2 as _return_code_pb2
from make87_messages_ros2.humble.shape_msgs.msg import plane_pb2 as _plane_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CalibrateBasePlaneRequest(_message.Message):
    __slots__ = ("header", "pose_frame", "robot_pose", "plane_estimation_method", "stereo_plane_preference", "region_of_interest_2d_id", "offset", "plane")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    POSE_FRAME_FIELD_NUMBER: _ClassVar[int]
    ROBOT_POSE_FIELD_NUMBER: _ClassVar[int]
    PLANE_ESTIMATION_METHOD_FIELD_NUMBER: _ClassVar[int]
    STEREO_PLANE_PREFERENCE_FIELD_NUMBER: _ClassVar[int]
    REGION_OF_INTEREST_2D_ID_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    PLANE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    pose_frame: str
    robot_pose: _pose_pb2.Pose
    plane_estimation_method: str
    stereo_plane_preference: str
    region_of_interest_2d_id: str
    offset: float
    plane: _plane_pb2.Plane
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., pose_frame: _Optional[str] = ..., robot_pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., plane_estimation_method: _Optional[str] = ..., stereo_plane_preference: _Optional[str] = ..., region_of_interest_2d_id: _Optional[str] = ..., offset: _Optional[float] = ..., plane: _Optional[_Union[_plane_pb2.Plane, _Mapping]] = ...) -> None: ...

class CalibrateBasePlaneResponse(_message.Message):
    __slots__ = ("header", "timestamp", "pose_frame", "plane", "return_code")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    POSE_FRAME_FIELD_NUMBER: _ClassVar[int]
    PLANE_FIELD_NUMBER: _ClassVar[int]
    RETURN_CODE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    timestamp: _time_pb2.Time
    pose_frame: str
    plane: _plane_pb2.Plane
    return_code: _return_code_pb2.ReturnCode
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., timestamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., pose_frame: _Optional[str] = ..., plane: _Optional[_Union[_plane_pb2.Plane, _Mapping]] = ..., return_code: _Optional[_Union[_return_code_pb2.ReturnCode, _Mapping]] = ...) -> None: ...
