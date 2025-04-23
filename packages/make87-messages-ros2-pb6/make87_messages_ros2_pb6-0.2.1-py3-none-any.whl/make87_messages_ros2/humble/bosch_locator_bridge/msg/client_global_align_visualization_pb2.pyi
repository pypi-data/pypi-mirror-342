from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.bosch_locator_bridge.msg import client_global_align_landmark_observation_notice_pb2 as _client_global_align_landmark_observation_notice_pb2
from make87_messages_ros2.humble.bosch_locator_bridge.msg import client_global_align_landmark_visualization_information_pb2 as _client_global_align_landmark_visualization_information_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClientGlobalAlignVisualization(_message.Message):
    __slots__ = ("header", "timestamp", "visualization_id", "landmarks", "observations")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VISUALIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    LANDMARKS_FIELD_NUMBER: _ClassVar[int]
    OBSERVATIONS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    timestamp: _time_pb2.Time
    visualization_id: int
    landmarks: _containers.RepeatedCompositeFieldContainer[_client_global_align_landmark_visualization_information_pb2.ClientGlobalAlignLandmarkVisualizationInformation]
    observations: _containers.RepeatedCompositeFieldContainer[_client_global_align_landmark_observation_notice_pb2.ClientGlobalAlignLandmarkObservationNotice]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., timestamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., visualization_id: _Optional[int] = ..., landmarks: _Optional[_Iterable[_Union[_client_global_align_landmark_visualization_information_pb2.ClientGlobalAlignLandmarkVisualizationInformation, _Mapping]]] = ..., observations: _Optional[_Iterable[_Union[_client_global_align_landmark_observation_notice_pb2.ClientGlobalAlignLandmarkObservationNotice, _Mapping]]] = ...) -> None: ...
