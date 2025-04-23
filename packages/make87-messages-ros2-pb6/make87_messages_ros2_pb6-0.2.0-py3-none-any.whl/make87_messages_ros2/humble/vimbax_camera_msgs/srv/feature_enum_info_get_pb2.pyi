from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.vimbax_camera_msgs.msg import error_pb2 as _error_pb2
from make87_messages_ros2.humble.vimbax_camera_msgs.msg import feature_module_pb2 as _feature_module_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FeatureEnumInfoGetRequest(_message.Message):
    __slots__ = ("header", "feature_name", "feature_module")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FEATURE_NAME_FIELD_NUMBER: _ClassVar[int]
    FEATURE_MODULE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    feature_name: str
    feature_module: _feature_module_pb2.FeatureModule
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., feature_name: _Optional[str] = ..., feature_module: _Optional[_Union[_feature_module_pb2.FeatureModule, _Mapping]] = ...) -> None: ...

class FeatureEnumInfoGetResponse(_message.Message):
    __slots__ = ("header", "possible_values", "available_values", "error")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    POSSIBLE_VALUES_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_VALUES_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    possible_values: _containers.RepeatedScalarFieldContainer[str]
    available_values: _containers.RepeatedScalarFieldContainer[str]
    error: _error_pb2.Error
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., possible_values: _Optional[_Iterable[str]] = ..., available_values: _Optional[_Iterable[str]] = ..., error: _Optional[_Union[_error_pb2.Error, _Mapping]] = ...) -> None: ...
