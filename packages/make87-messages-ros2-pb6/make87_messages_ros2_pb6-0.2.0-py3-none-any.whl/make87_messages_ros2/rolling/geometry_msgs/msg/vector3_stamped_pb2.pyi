from make87_messages_ros2.rolling.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Vector3Stamped(_message.Message):
    __slots__ = ("header", "vector")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VECTOR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    vector: _vector3_pb2.Vector3
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., vector: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ...) -> None: ...
