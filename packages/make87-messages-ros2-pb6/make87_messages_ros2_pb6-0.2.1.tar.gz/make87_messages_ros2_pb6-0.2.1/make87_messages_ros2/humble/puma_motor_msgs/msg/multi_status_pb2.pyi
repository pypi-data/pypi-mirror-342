from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.puma_motor_msgs.msg import status_pb2 as _status_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MultiStatus(_message.Message):
    __slots__ = ("header", "ros2_header", "drivers")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    DRIVERS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    drivers: _containers.RepeatedCompositeFieldContainer[_status_pb2.Status]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., drivers: _Optional[_Iterable[_Union[_status_pb2.Status, _Mapping]]] = ...) -> None: ...
