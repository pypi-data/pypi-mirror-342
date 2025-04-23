from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import color_rgba_pb2 as _color_rgba_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetLightPropertiesRequest(_message.Message):
    __slots__ = ("header", "light_name", "diffuse", "attenuation_constant", "attenuation_linear", "attenuation_quadratic")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LIGHT_NAME_FIELD_NUMBER: _ClassVar[int]
    DIFFUSE_FIELD_NUMBER: _ClassVar[int]
    ATTENUATION_CONSTANT_FIELD_NUMBER: _ClassVar[int]
    ATTENUATION_LINEAR_FIELD_NUMBER: _ClassVar[int]
    ATTENUATION_QUADRATIC_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    light_name: str
    diffuse: _color_rgba_pb2.ColorRGBA
    attenuation_constant: float
    attenuation_linear: float
    attenuation_quadratic: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., light_name: _Optional[str] = ..., diffuse: _Optional[_Union[_color_rgba_pb2.ColorRGBA, _Mapping]] = ..., attenuation_constant: _Optional[float] = ..., attenuation_linear: _Optional[float] = ..., attenuation_quadratic: _Optional[float] = ...) -> None: ...

class SetLightPropertiesResponse(_message.Message):
    __slots__ = ("header", "success", "status_message")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    status_message: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., status_message: _Optional[str] = ...) -> None: ...
