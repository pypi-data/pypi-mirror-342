from make87_messages_ros2.rolling.ublox_msgs.msg import mon_ver_extension_pb2 as _mon_ver_extension_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MonVER(_message.Message):
    __slots__ = ("sw_version", "hw_version", "extension")
    SW_VERSION_FIELD_NUMBER: _ClassVar[int]
    HW_VERSION_FIELD_NUMBER: _ClassVar[int]
    EXTENSION_FIELD_NUMBER: _ClassVar[int]
    sw_version: _containers.RepeatedScalarFieldContainer[int]
    hw_version: _containers.RepeatedScalarFieldContainer[int]
    extension: _containers.RepeatedCompositeFieldContainer[_mon_ver_extension_pb2.MonVERExtension]
    def __init__(self, sw_version: _Optional[_Iterable[int]] = ..., hw_version: _Optional[_Iterable[int]] = ..., extension: _Optional[_Iterable[_Union[_mon_ver_extension_pb2.MonVERExtension, _Mapping]]] = ...) -> None: ...
