from make87_messages_ros2.jazzy.flexbe_msgs.msg import userdata_info_pb2 as _userdata_info_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetUserdataRequest(_message.Message):
    __slots__ = ("userdata_key",)
    USERDATA_KEY_FIELD_NUMBER: _ClassVar[int]
    userdata_key: str
    def __init__(self, userdata_key: _Optional[str] = ...) -> None: ...

class GetUserdataResponse(_message.Message):
    __slots__ = ("success", "message", "userdata")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    USERDATA_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    userdata: _containers.RepeatedCompositeFieldContainer[_userdata_info_pb2.UserdataInfo]
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., userdata: _Optional[_Iterable[_Union[_userdata_info_pb2.UserdataInfo, _Mapping]]] = ...) -> None: ...
