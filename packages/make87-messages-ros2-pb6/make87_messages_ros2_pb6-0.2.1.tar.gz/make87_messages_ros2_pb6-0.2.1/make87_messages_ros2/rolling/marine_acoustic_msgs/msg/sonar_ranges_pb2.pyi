from make87_messages_ros2.rolling.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.rolling.marine_acoustic_msgs.msg import detection_flag_pb2 as _detection_flag_pb2
from make87_messages_ros2.rolling.marine_acoustic_msgs.msg import ping_info_pb2 as _ping_info_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SonarRanges(_message.Message):
    __slots__ = ("header", "ping_info", "flags", "transmit_delays", "intensities", "beam_unit_vec", "ranges")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PING_INFO_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    TRANSMIT_DELAYS_FIELD_NUMBER: _ClassVar[int]
    INTENSITIES_FIELD_NUMBER: _ClassVar[int]
    BEAM_UNIT_VEC_FIELD_NUMBER: _ClassVar[int]
    RANGES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ping_info: _ping_info_pb2.PingInfo
    flags: _containers.RepeatedCompositeFieldContainer[_detection_flag_pb2.DetectionFlag]
    transmit_delays: _containers.RepeatedScalarFieldContainer[float]
    intensities: _containers.RepeatedScalarFieldContainer[float]
    beam_unit_vec: _containers.RepeatedCompositeFieldContainer[_vector3_pb2.Vector3]
    ranges: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ping_info: _Optional[_Union[_ping_info_pb2.PingInfo, _Mapping]] = ..., flags: _Optional[_Iterable[_Union[_detection_flag_pb2.DetectionFlag, _Mapping]]] = ..., transmit_delays: _Optional[_Iterable[float]] = ..., intensities: _Optional[_Iterable[float]] = ..., beam_unit_vec: _Optional[_Iterable[_Union[_vector3_pb2.Vector3, _Mapping]]] = ..., ranges: _Optional[_Iterable[float]] = ...) -> None: ...
