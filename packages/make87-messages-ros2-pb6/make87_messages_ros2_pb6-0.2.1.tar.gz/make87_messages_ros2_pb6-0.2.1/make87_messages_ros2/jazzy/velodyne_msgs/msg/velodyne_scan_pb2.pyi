from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.jazzy.velodyne_msgs.msg import velodyne_packet_pb2 as _velodyne_packet_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VelodyneScan(_message.Message):
    __slots__ = ("header", "packets")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PACKETS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    packets: _containers.RepeatedCompositeFieldContainer[_velodyne_packet_pb2.VelodynePacket]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., packets: _Optional[_Iterable[_Union[_velodyne_packet_pb2.VelodynePacket, _Mapping]]] = ...) -> None: ...
