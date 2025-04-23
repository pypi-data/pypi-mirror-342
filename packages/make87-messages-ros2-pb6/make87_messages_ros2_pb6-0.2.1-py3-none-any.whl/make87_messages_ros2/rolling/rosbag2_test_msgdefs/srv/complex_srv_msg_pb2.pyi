from make87_messages_ros2.rolling.rosbag2_test_msgdefs.msg import basic_msg_pb2 as _basic_msg_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ComplexSrvMsgRequest(_message.Message):
    __slots__ = ("req",)
    REQ_FIELD_NUMBER: _ClassVar[int]
    req: _basic_msg_pb2.BasicMsg
    def __init__(self, req: _Optional[_Union[_basic_msg_pb2.BasicMsg, _Mapping]] = ...) -> None: ...

class ComplexSrvMsgResponse(_message.Message):
    __slots__ = ("resp",)
    RESP_FIELD_NUMBER: _ClassVar[int]
    resp: _basic_msg_pb2.BasicMsg
    def __init__(self, resp: _Optional[_Union[_basic_msg_pb2.BasicMsg, _Mapping]] = ...) -> None: ...
