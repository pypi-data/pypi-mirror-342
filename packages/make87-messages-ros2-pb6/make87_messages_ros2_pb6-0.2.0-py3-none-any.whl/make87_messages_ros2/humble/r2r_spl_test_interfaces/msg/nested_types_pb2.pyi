from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.r2r_spl_test_interfaces.msg import basic_types_pb2 as _basic_types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NestedTypes(_message.Message):
    __slots__ = ("header", "data_basic_types", "data_basic_types_array")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DATA_BASIC_TYPES_FIELD_NUMBER: _ClassVar[int]
    DATA_BASIC_TYPES_ARRAY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    data_basic_types: _basic_types_pb2.BasicTypes
    data_basic_types_array: _containers.RepeatedCompositeFieldContainer[_basic_types_pb2.BasicTypes]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., data_basic_types: _Optional[_Union[_basic_types_pb2.BasicTypes, _Mapping]] = ..., data_basic_types_array: _Optional[_Iterable[_Union[_basic_types_pb2.BasicTypes, _Mapping]]] = ...) -> None: ...
