from make87_messages_ros2.rolling.builtin_interfaces.msg import duration_pb2 as _duration_pb2
from make87_messages_ros2.rolling.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.rolling.geometry_msgs.msg import point_pb2 as _point_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TestMessage(_message.Message):
    __slots__ = ("header", "b", "ui8", "ui16", "ui32", "ui64", "i8", "i16", "i32", "i64", "f32", "f64", "str", "bounded_str", "t", "d", "point_arr")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    B_FIELD_NUMBER: _ClassVar[int]
    UI8_FIELD_NUMBER: _ClassVar[int]
    UI16_FIELD_NUMBER: _ClassVar[int]
    UI32_FIELD_NUMBER: _ClassVar[int]
    UI64_FIELD_NUMBER: _ClassVar[int]
    I8_FIELD_NUMBER: _ClassVar[int]
    I16_FIELD_NUMBER: _ClassVar[int]
    I32_FIELD_NUMBER: _ClassVar[int]
    I64_FIELD_NUMBER: _ClassVar[int]
    F32_FIELD_NUMBER: _ClassVar[int]
    F64_FIELD_NUMBER: _ClassVar[int]
    STR_FIELD_NUMBER: _ClassVar[int]
    BOUNDED_STR_FIELD_NUMBER: _ClassVar[int]
    T_FIELD_NUMBER: _ClassVar[int]
    D_FIELD_NUMBER: _ClassVar[int]
    POINT_ARR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    b: bool
    ui8: int
    ui16: int
    ui32: int
    ui64: int
    i8: int
    i16: int
    i32: int
    i64: int
    f32: float
    f64: float
    str: str
    bounded_str: str
    t: _time_pb2.Time
    d: _duration_pb2.Duration
    point_arr: _containers.RepeatedCompositeFieldContainer[_point_pb2.Point]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., b: bool = ..., ui8: _Optional[int] = ..., ui16: _Optional[int] = ..., ui32: _Optional[int] = ..., ui64: _Optional[int] = ..., i8: _Optional[int] = ..., i16: _Optional[int] = ..., i32: _Optional[int] = ..., i64: _Optional[int] = ..., f32: _Optional[float] = ..., f64: _Optional[float] = ..., str: _Optional[str] = ..., bounded_str: _Optional[str] = ..., t: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., d: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., point_arr: _Optional[_Iterable[_Union[_point_pb2.Point, _Mapping]]] = ...) -> None: ...
