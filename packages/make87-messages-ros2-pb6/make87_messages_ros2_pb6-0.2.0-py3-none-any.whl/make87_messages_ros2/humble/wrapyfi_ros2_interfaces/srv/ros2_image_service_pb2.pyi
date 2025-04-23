from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import image_pb2 as _image_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ROS2ImageServiceRequest(_message.Message):
    __slots__ = ("header", "request")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    request: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., request: _Optional[str] = ...) -> None: ...

class ROS2ImageServiceResponse(_message.Message):
    __slots__ = ("header", "response")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    response: _image_pb2.Image
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., response: _Optional[_Union[_image_pb2.Image, _Mapping]] = ...) -> None: ...
