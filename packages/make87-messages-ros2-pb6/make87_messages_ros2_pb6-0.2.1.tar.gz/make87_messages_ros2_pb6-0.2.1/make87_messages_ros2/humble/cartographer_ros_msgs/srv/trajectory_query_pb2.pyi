from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.cartographer_ros_msgs.msg import status_response_pb2 as _status_response_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_stamped_pb2 as _pose_stamped_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TrajectoryQueryRequest(_message.Message):
    __slots__ = ("header", "trajectory_id")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TRAJECTORY_ID_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    trajectory_id: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., trajectory_id: _Optional[int] = ...) -> None: ...

class TrajectoryQueryResponse(_message.Message):
    __slots__ = ("header", "status", "trajectory")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TRAJECTORY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    status: _status_response_pb2.StatusResponse
    trajectory: _containers.RepeatedCompositeFieldContainer[_pose_stamped_pb2.PoseStamped]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., status: _Optional[_Union[_status_response_pb2.StatusResponse, _Mapping]] = ..., trajectory: _Optional[_Iterable[_Union[_pose_stamped_pb2.PoseStamped, _Mapping]]] = ...) -> None: ...
