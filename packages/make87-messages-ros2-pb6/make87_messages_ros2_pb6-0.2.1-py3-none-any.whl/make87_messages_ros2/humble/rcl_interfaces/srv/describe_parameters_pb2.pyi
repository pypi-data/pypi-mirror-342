from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rcl_interfaces.msg import parameter_descriptor_pb2 as _parameter_descriptor_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DescribeParametersRequest(_message.Message):
    __slots__ = ("header", "names")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAMES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., names: _Optional[_Iterable[str]] = ...) -> None: ...

class DescribeParametersResponse(_message.Message):
    __slots__ = ("header", "descriptors")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTORS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    descriptors: _containers.RepeatedCompositeFieldContainer[_parameter_descriptor_pb2.ParameterDescriptor]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., descriptors: _Optional[_Iterable[_Union[_parameter_descriptor_pb2.ParameterDescriptor, _Mapping]]] = ...) -> None: ...
