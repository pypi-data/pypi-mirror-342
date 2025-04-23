from make87_messages_ros2.jazzy.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Vibration(_message.Message):
    __slots__ = ("header", "vibration", "clipping")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VIBRATION_FIELD_NUMBER: _ClassVar[int]
    CLIPPING_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    vibration: _vector3_pb2.Vector3
    clipping: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., vibration: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., clipping: _Optional[_Iterable[float]] = ...) -> None: ...
