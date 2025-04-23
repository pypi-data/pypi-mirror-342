from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.as2_msgs.msg import node_status_pb2 as _node_status_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TrajGenInfo(_message.Message):
    __slots__ = ("header", "ros2_header", "node_status", "active_status")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    NODE_STATUS_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_STATUS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    node_status: _node_status_pb2.NodeStatus
    active_status: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., node_status: _Optional[_Union[_node_status_pb2.NodeStatus, _Mapping]] = ..., active_status: _Optional[int] = ...) -> None: ...
