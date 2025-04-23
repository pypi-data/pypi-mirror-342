from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.gazebo_msgs.msg import link_state_pb2 as _link_state_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetLinkStateRequest(_message.Message):
    __slots__ = ("header", "link_state")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LINK_STATE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    link_state: _link_state_pb2.LinkState
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., link_state: _Optional[_Union[_link_state_pb2.LinkState, _Mapping]] = ...) -> None: ...

class SetLinkStateResponse(_message.Message):
    __slots__ = ("header", "success", "status_message")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    status_message: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., status_message: _Optional[str] = ...) -> None: ...
