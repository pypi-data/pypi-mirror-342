from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.qb_softhand_industry_msgs.msg import resource_data_pb2 as _resource_data_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class State(_message.Message):
    __slots__ = ("header", "actuator")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ACTUATOR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    actuator: _resource_data_pb2.ResourceData
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., actuator: _Optional[_Union[_resource_data_pb2.ResourceData, _Mapping]] = ...) -> None: ...
