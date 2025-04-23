from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rosbridge_msgs.msg import connected_client_pb2 as _connected_client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ConnectedClients(_message.Message):
    __slots__ = ("header", "clients")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CLIENTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    clients: _containers.RepeatedCompositeFieldContainer[_connected_client_pb2.ConnectedClient]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., clients: _Optional[_Iterable[_Union[_connected_client_pb2.ConnectedClient, _Mapping]]] = ...) -> None: ...
