from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SensorNoise(_message.Message):
    __slots__ = ("header", "type", "mean", "stddev", "bias_mean", "bias_stddev", "precision", "dynamic_bias_stddev", "dynamic_bias_correlation_time")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    MEAN_FIELD_NUMBER: _ClassVar[int]
    STDDEV_FIELD_NUMBER: _ClassVar[int]
    BIAS_MEAN_FIELD_NUMBER: _ClassVar[int]
    BIAS_STDDEV_FIELD_NUMBER: _ClassVar[int]
    PRECISION_FIELD_NUMBER: _ClassVar[int]
    DYNAMIC_BIAS_STDDEV_FIELD_NUMBER: _ClassVar[int]
    DYNAMIC_BIAS_CORRELATION_TIME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    type: int
    mean: float
    stddev: float
    bias_mean: float
    bias_stddev: float
    precision: float
    dynamic_bias_stddev: float
    dynamic_bias_correlation_time: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., type: _Optional[int] = ..., mean: _Optional[float] = ..., stddev: _Optional[float] = ..., bias_mean: _Optional[float] = ..., bias_stddev: _Optional[float] = ..., precision: _Optional[float] = ..., dynamic_bias_stddev: _Optional[float] = ..., dynamic_bias_correlation_time: _Optional[float] = ...) -> None: ...
