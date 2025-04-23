from make87_messages_ros2.rolling.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.rolling.cartographer_ros_msgs.msg import metric_family_pb2 as _metric_family_pb2
from make87_messages_ros2.rolling.cartographer_ros_msgs.msg import status_response_pb2 as _status_response_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ReadMetricsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ReadMetricsResponse(_message.Message):
    __slots__ = ("status", "metric_families", "timestamp")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    METRIC_FAMILIES_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    status: _status_response_pb2.StatusResponse
    metric_families: _containers.RepeatedCompositeFieldContainer[_metric_family_pb2.MetricFamily]
    timestamp: _time_pb2.Time
    def __init__(self, status: _Optional[_Union[_status_response_pb2.StatusResponse, _Mapping]] = ..., metric_families: _Optional[_Iterable[_Union[_metric_family_pb2.MetricFamily, _Mapping]]] = ..., timestamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ...) -> None: ...
