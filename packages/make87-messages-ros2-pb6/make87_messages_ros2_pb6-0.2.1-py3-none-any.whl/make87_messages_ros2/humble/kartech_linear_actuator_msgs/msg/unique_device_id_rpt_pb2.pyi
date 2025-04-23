from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UniqueDeviceIdRpt(_message.Message):
    __slots__ = ("header", "ros2_header", "actuator_id_first_6", "actuator_id_last_6")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    ACTUATOR_ID_FIRST_6_FIELD_NUMBER: _ClassVar[int]
    ACTUATOR_ID_LAST_6_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    actuator_id_first_6: int
    actuator_id_last_6: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., actuator_id_first_6: _Optional[int] = ..., actuator_id_last_6: _Optional[int] = ...) -> None: ...
