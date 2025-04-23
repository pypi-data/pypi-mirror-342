from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.ublox_msgs.msg import mon_ver_extension_pb2 as _mon_ver_extension_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MonVER(_message.Message):
    __slots__ = ("header", "sw_version", "hw_version", "extension")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SW_VERSION_FIELD_NUMBER: _ClassVar[int]
    HW_VERSION_FIELD_NUMBER: _ClassVar[int]
    EXTENSION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    sw_version: _containers.RepeatedScalarFieldContainer[int]
    hw_version: _containers.RepeatedScalarFieldContainer[int]
    extension: _containers.RepeatedCompositeFieldContainer[_mon_ver_extension_pb2.MonVERExtension]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., sw_version: _Optional[_Iterable[int]] = ..., hw_version: _Optional[_Iterable[int]] = ..., extension: _Optional[_Iterable[_Union[_mon_ver_extension_pb2.MonVERExtension, _Mapping]]] = ...) -> None: ...
