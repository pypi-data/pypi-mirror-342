from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AftermarketLane(_message.Message):
    __slots__ = ("header", "lane_confidence_left", "ldw_available_left", "lane_type_left", "distance_to_left_lane", "lane_confidence_right", "ldw_available_right", "lane_type_right", "distance_to_right_lane")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LANE_CONFIDENCE_LEFT_FIELD_NUMBER: _ClassVar[int]
    LDW_AVAILABLE_LEFT_FIELD_NUMBER: _ClassVar[int]
    LANE_TYPE_LEFT_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_TO_LEFT_LANE_FIELD_NUMBER: _ClassVar[int]
    LANE_CONFIDENCE_RIGHT_FIELD_NUMBER: _ClassVar[int]
    LDW_AVAILABLE_RIGHT_FIELD_NUMBER: _ClassVar[int]
    LANE_TYPE_RIGHT_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_TO_RIGHT_LANE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    lane_confidence_left: int
    ldw_available_left: bool
    lane_type_left: int
    distance_to_left_lane: float
    lane_confidence_right: int
    ldw_available_right: bool
    lane_type_right: int
    distance_to_right_lane: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., lane_confidence_left: _Optional[int] = ..., ldw_available_left: bool = ..., lane_type_left: _Optional[int] = ..., distance_to_left_lane: _Optional[float] = ..., lane_confidence_right: _Optional[int] = ..., ldw_available_right: bool = ..., lane_type_right: _Optional[int] = ..., distance_to_right_lane: _Optional[float] = ...) -> None: ...
