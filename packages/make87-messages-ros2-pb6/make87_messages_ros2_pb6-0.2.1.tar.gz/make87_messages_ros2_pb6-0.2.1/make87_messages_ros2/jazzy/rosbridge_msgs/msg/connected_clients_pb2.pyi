from make87_messages_ros2.jazzy.rosbridge_msgs.msg import connected_client_pb2 as _connected_client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ConnectedClients(_message.Message):
    __slots__ = ("clients",)
    CLIENTS_FIELD_NUMBER: _ClassVar[int]
    clients: _containers.RepeatedCompositeFieldContainer[_connected_client_pb2.ConnectedClient]
    def __init__(self, clients: _Optional[_Iterable[_Union[_connected_client_pb2.ConnectedClient, _Mapping]]] = ...) -> None: ...
