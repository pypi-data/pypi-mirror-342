from make87_messages_ros2.rolling.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DifferentialMeasurement(_message.Message):
    __slots__ = ("header", "base_frame_id", "baseline_length", "baseline_length_variance", "heading", "heading_variance", "pitch", "pitch_variance", "roll", "roll_variance", "position", "position_covariance")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BASE_FRAME_ID_FIELD_NUMBER: _ClassVar[int]
    BASELINE_LENGTH_FIELD_NUMBER: _ClassVar[int]
    BASELINE_LENGTH_VARIANCE_FIELD_NUMBER: _ClassVar[int]
    HEADING_FIELD_NUMBER: _ClassVar[int]
    HEADING_VARIANCE_FIELD_NUMBER: _ClassVar[int]
    PITCH_FIELD_NUMBER: _ClassVar[int]
    PITCH_VARIANCE_FIELD_NUMBER: _ClassVar[int]
    ROLL_FIELD_NUMBER: _ClassVar[int]
    ROLL_VARIANCE_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    POSITION_COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    base_frame_id: str
    baseline_length: float
    baseline_length_variance: float
    heading: float
    heading_variance: float
    pitch: float
    pitch_variance: float
    roll: float
    roll_variance: float
    position: _vector3_pb2.Vector3
    position_covariance: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., base_frame_id: _Optional[str] = ..., baseline_length: _Optional[float] = ..., baseline_length_variance: _Optional[float] = ..., heading: _Optional[float] = ..., heading_variance: _Optional[float] = ..., pitch: _Optional[float] = ..., pitch_variance: _Optional[float] = ..., roll: _Optional[float] = ..., roll_variance: _Optional[float] = ..., position: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., position_covariance: _Optional[_Iterable[float]] = ...) -> None: ...
