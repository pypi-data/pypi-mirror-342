from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.wireless_msgs.msg import network_pb2 as _network_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Scan(_message.Message):
    __slots__ = ("header", "networks")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NETWORKS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    networks: _containers.RepeatedCompositeFieldContainer[_network_pb2.Network]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., networks: _Optional[_Iterable[_Union[_network_pb2.Network, _Mapping]]] = ...) -> None: ...
