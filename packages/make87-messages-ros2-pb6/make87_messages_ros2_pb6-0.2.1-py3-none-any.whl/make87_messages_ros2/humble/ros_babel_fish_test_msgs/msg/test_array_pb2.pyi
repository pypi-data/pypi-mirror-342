from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import duration_pb2 as _duration_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.humble.ros_babel_fish_test_msgs.msg import test_sub_array_pb2 as _test_sub_array_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TestArray(_message.Message):
    __slots__ = ("header", "bools", "uint8s", "uint16s", "uint32s", "uint64s", "int8s", "int16s", "int32s", "int64s", "float32s", "float64s", "times", "durations", "strings", "subarrays_fixed", "subarrays")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BOOLS_FIELD_NUMBER: _ClassVar[int]
    UINT8S_FIELD_NUMBER: _ClassVar[int]
    UINT16S_FIELD_NUMBER: _ClassVar[int]
    UINT32S_FIELD_NUMBER: _ClassVar[int]
    UINT64S_FIELD_NUMBER: _ClassVar[int]
    INT8S_FIELD_NUMBER: _ClassVar[int]
    INT16S_FIELD_NUMBER: _ClassVar[int]
    INT32S_FIELD_NUMBER: _ClassVar[int]
    INT64S_FIELD_NUMBER: _ClassVar[int]
    FLOAT32S_FIELD_NUMBER: _ClassVar[int]
    FLOAT64S_FIELD_NUMBER: _ClassVar[int]
    TIMES_FIELD_NUMBER: _ClassVar[int]
    DURATIONS_FIELD_NUMBER: _ClassVar[int]
    STRINGS_FIELD_NUMBER: _ClassVar[int]
    SUBARRAYS_FIXED_FIELD_NUMBER: _ClassVar[int]
    SUBARRAYS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    bools: _containers.RepeatedScalarFieldContainer[bool]
    uint8s: _containers.RepeatedScalarFieldContainer[int]
    uint16s: _containers.RepeatedScalarFieldContainer[int]
    uint32s: _containers.RepeatedScalarFieldContainer[int]
    uint64s: _containers.RepeatedScalarFieldContainer[int]
    int8s: _containers.RepeatedScalarFieldContainer[int]
    int16s: _containers.RepeatedScalarFieldContainer[int]
    int32s: _containers.RepeatedScalarFieldContainer[int]
    int64s: _containers.RepeatedScalarFieldContainer[int]
    float32s: _containers.RepeatedScalarFieldContainer[float]
    float64s: _containers.RepeatedScalarFieldContainer[float]
    times: _containers.RepeatedCompositeFieldContainer[_time_pb2.Time]
    durations: _containers.RepeatedCompositeFieldContainer[_duration_pb2.Duration]
    strings: _containers.RepeatedScalarFieldContainer[str]
    subarrays_fixed: _containers.RepeatedCompositeFieldContainer[_test_sub_array_pb2.TestSubArray]
    subarrays: _containers.RepeatedCompositeFieldContainer[_test_sub_array_pb2.TestSubArray]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., bools: _Optional[_Iterable[bool]] = ..., uint8s: _Optional[_Iterable[int]] = ..., uint16s: _Optional[_Iterable[int]] = ..., uint32s: _Optional[_Iterable[int]] = ..., uint64s: _Optional[_Iterable[int]] = ..., int8s: _Optional[_Iterable[int]] = ..., int16s: _Optional[_Iterable[int]] = ..., int32s: _Optional[_Iterable[int]] = ..., int64s: _Optional[_Iterable[int]] = ..., float32s: _Optional[_Iterable[float]] = ..., float64s: _Optional[_Iterable[float]] = ..., times: _Optional[_Iterable[_Union[_time_pb2.Time, _Mapping]]] = ..., durations: _Optional[_Iterable[_Union[_duration_pb2.Duration, _Mapping]]] = ..., strings: _Optional[_Iterable[str]] = ..., subarrays_fixed: _Optional[_Iterable[_Union[_test_sub_array_pb2.TestSubArray, _Mapping]]] = ..., subarrays: _Optional[_Iterable[_Union[_test_sub_array_pb2.TestSubArray, _Mapping]]] = ...) -> None: ...
