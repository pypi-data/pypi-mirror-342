from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LkaLane(_message.Message):
    __slots__ = ("header", "ros2_header", "lane_type", "quality", "model_degree", "position_parameter_c0", "curvature_parameter_c2", "curvature_derivative_parameter_c3", "marking_width", "heading_angle_parameter_c1", "view_range", "view_range_availability")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    LANE_TYPE_FIELD_NUMBER: _ClassVar[int]
    QUALITY_FIELD_NUMBER: _ClassVar[int]
    MODEL_DEGREE_FIELD_NUMBER: _ClassVar[int]
    POSITION_PARAMETER_C0_FIELD_NUMBER: _ClassVar[int]
    CURVATURE_PARAMETER_C2_FIELD_NUMBER: _ClassVar[int]
    CURVATURE_DERIVATIVE_PARAMETER_C3_FIELD_NUMBER: _ClassVar[int]
    MARKING_WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEADING_ANGLE_PARAMETER_C1_FIELD_NUMBER: _ClassVar[int]
    VIEW_RANGE_FIELD_NUMBER: _ClassVar[int]
    VIEW_RANGE_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    lane_type: int
    quality: int
    model_degree: int
    position_parameter_c0: float
    curvature_parameter_c2: float
    curvature_derivative_parameter_c3: float
    marking_width: float
    heading_angle_parameter_c1: float
    view_range: float
    view_range_availability: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., lane_type: _Optional[int] = ..., quality: _Optional[int] = ..., model_degree: _Optional[int] = ..., position_parameter_c0: _Optional[float] = ..., curvature_parameter_c2: _Optional[float] = ..., curvature_derivative_parameter_c3: _Optional[float] = ..., marking_width: _Optional[float] = ..., heading_angle_parameter_c1: _Optional[float] = ..., view_range: _Optional[float] = ..., view_range_availability: bool = ...) -> None: ...
