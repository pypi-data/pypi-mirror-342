from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.jazzy.rc_common_msgs.msg import return_code_pb2 as _return_code_pb2
from make87_messages_ros2.jazzy.rc_reason_msgs.msg import collision_detection_pb2 as _collision_detection_pb2
from make87_messages_ros2.jazzy.rc_reason_msgs.msg import grasp_pb2 as _grasp_pb2
from make87_messages_ros2.jazzy.rc_reason_msgs.msg import load_carrier_pb2 as _load_carrier_pb2
from make87_messages_ros2.jazzy.rc_reason_msgs.msg import match_pb2 as _match_pb2
from make87_messages_ros2.jazzy.rc_reason_msgs.msg import silhouette_match_object_pb2 as _silhouette_match_object_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SilhouetteMatchDetectObjectRequest(_message.Message):
    __slots__ = ("object_to_detect", "offset", "pose_frame", "robot_pose", "load_carrier_id", "collision_detection", "object_plane_detection")
    OBJECT_TO_DETECT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    POSE_FRAME_FIELD_NUMBER: _ClassVar[int]
    ROBOT_POSE_FIELD_NUMBER: _ClassVar[int]
    LOAD_CARRIER_ID_FIELD_NUMBER: _ClassVar[int]
    COLLISION_DETECTION_FIELD_NUMBER: _ClassVar[int]
    OBJECT_PLANE_DETECTION_FIELD_NUMBER: _ClassVar[int]
    object_to_detect: _silhouette_match_object_pb2.SilhouetteMatchObject
    offset: float
    pose_frame: str
    robot_pose: _pose_pb2.Pose
    load_carrier_id: str
    collision_detection: _collision_detection_pb2.CollisionDetection
    object_plane_detection: bool
    def __init__(self, object_to_detect: _Optional[_Union[_silhouette_match_object_pb2.SilhouetteMatchObject, _Mapping]] = ..., offset: _Optional[float] = ..., pose_frame: _Optional[str] = ..., robot_pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., load_carrier_id: _Optional[str] = ..., collision_detection: _Optional[_Union[_collision_detection_pb2.CollisionDetection, _Mapping]] = ..., object_plane_detection: bool = ...) -> None: ...

class SilhouetteMatchDetectObjectResponse(_message.Message):
    __slots__ = ("timestamp", "object_id", "matches", "grasps", "load_carriers", "return_code")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    MATCHES_FIELD_NUMBER: _ClassVar[int]
    GRASPS_FIELD_NUMBER: _ClassVar[int]
    LOAD_CARRIERS_FIELD_NUMBER: _ClassVar[int]
    RETURN_CODE_FIELD_NUMBER: _ClassVar[int]
    timestamp: _time_pb2.Time
    object_id: str
    matches: _containers.RepeatedCompositeFieldContainer[_match_pb2.Match]
    grasps: _containers.RepeatedCompositeFieldContainer[_grasp_pb2.Grasp]
    load_carriers: _containers.RepeatedCompositeFieldContainer[_load_carrier_pb2.LoadCarrier]
    return_code: _return_code_pb2.ReturnCode
    def __init__(self, timestamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., object_id: _Optional[str] = ..., matches: _Optional[_Iterable[_Union[_match_pb2.Match, _Mapping]]] = ..., grasps: _Optional[_Iterable[_Union[_grasp_pb2.Grasp, _Mapping]]] = ..., load_carriers: _Optional[_Iterable[_Union[_load_carrier_pb2.LoadCarrier, _Mapping]]] = ..., return_code: _Optional[_Union[_return_code_pb2.ReturnCode, _Mapping]] = ...) -> None: ...
