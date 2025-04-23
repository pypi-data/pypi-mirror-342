from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.novatel_gps_msgs.msg import satellite_pb2 as _satellite_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Gpgsv(_message.Message):
    __slots__ = ("header", "ros2_header", "message_id", "n_msgs", "msg_number", "n_satellites", "satellites")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    N_MSGS_FIELD_NUMBER: _ClassVar[int]
    MSG_NUMBER_FIELD_NUMBER: _ClassVar[int]
    N_SATELLITES_FIELD_NUMBER: _ClassVar[int]
    SATELLITES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    message_id: str
    n_msgs: int
    msg_number: int
    n_satellites: int
    satellites: _containers.RepeatedCompositeFieldContainer[_satellite_pb2.Satellite]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., message_id: _Optional[str] = ..., n_msgs: _Optional[int] = ..., msg_number: _Optional[int] = ..., n_satellites: _Optional[int] = ..., satellites: _Optional[_Iterable[_Union[_satellite_pb2.Satellite, _Mapping]]] = ...) -> None: ...
