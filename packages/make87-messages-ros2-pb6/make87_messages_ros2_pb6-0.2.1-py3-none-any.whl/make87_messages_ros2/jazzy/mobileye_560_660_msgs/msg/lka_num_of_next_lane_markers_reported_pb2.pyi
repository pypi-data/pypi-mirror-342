from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LkaNumOfNextLaneMarkersReported(_message.Message):
    __slots__ = ("header", "num_of_next_lane_markers_reported")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NUM_OF_NEXT_LANE_MARKERS_REPORTED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    num_of_next_lane_markers_reported: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., num_of_next_lane_markers_reported: _Optional[int] = ...) -> None: ...
