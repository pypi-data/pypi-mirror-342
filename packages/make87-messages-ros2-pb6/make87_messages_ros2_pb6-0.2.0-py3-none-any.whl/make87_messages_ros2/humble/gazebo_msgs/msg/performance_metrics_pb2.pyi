from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.gazebo_msgs.msg import sensor_performance_metric_pb2 as _sensor_performance_metric_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PerformanceMetrics(_message.Message):
    __slots__ = ("header", "ros2_header", "real_time_factor", "sensors")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    REAL_TIME_FACTOR_FIELD_NUMBER: _ClassVar[int]
    SENSORS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    real_time_factor: float
    sensors: _containers.RepeatedCompositeFieldContainer[_sensor_performance_metric_pb2.SensorPerformanceMetric]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., real_time_factor: _Optional[float] = ..., sensors: _Optional[_Iterable[_Union[_sensor_performance_metric_pb2.SensorPerformanceMetric, _Mapping]]] = ...) -> None: ...
