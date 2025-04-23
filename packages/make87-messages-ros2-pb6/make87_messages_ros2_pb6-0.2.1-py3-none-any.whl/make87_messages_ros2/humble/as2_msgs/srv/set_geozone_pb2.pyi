from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.as2_msgs.msg import geozone_pb2 as _geozone_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetGeozoneRequest(_message.Message):
    __slots__ = ("header", "geozone")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    GEOZONE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    geozone: _geozone_pb2.Geozone
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., geozone: _Optional[_Union[_geozone_pb2.Geozone, _Mapping]] = ...) -> None: ...

class SetGeozoneResponse(_message.Message):
    __slots__ = ("header", "success")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ...) -> None: ...
