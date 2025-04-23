from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rosbag2_storage_mcap_testdata.msg import basic_msg_pb2 as _basic_msg_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ComplexMsg(_message.Message):
    __slots__ = ("header", "b")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    B_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    b: _basic_msg_pb2.BasicMsg
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., b: _Optional[_Union[_basic_msg_pb2.BasicMsg, _Mapping]] = ...) -> None: ...
