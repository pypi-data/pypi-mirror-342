from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AnsToCmdConnect(_message.Message):
    __slots__ = ("header", "ros2_header", "command", "cmd_connect_ans_d7", "cmd_connect_ans_d6", "cmd_connect_ans_d5", "cmd_connect_ans_d4", "cmd_connect_ans_d3", "cmd_connect_ans_d2", "cmd_connect_ans_d1")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    CMD_CONNECT_ANS_D7_FIELD_NUMBER: _ClassVar[int]
    CMD_CONNECT_ANS_D6_FIELD_NUMBER: _ClassVar[int]
    CMD_CONNECT_ANS_D5_FIELD_NUMBER: _ClassVar[int]
    CMD_CONNECT_ANS_D4_FIELD_NUMBER: _ClassVar[int]
    CMD_CONNECT_ANS_D3_FIELD_NUMBER: _ClassVar[int]
    CMD_CONNECT_ANS_D2_FIELD_NUMBER: _ClassVar[int]
    CMD_CONNECT_ANS_D1_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    command: int
    cmd_connect_ans_d7: int
    cmd_connect_ans_d6: int
    cmd_connect_ans_d5: int
    cmd_connect_ans_d4: int
    cmd_connect_ans_d3: int
    cmd_connect_ans_d2: int
    cmd_connect_ans_d1: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., command: _Optional[int] = ..., cmd_connect_ans_d7: _Optional[int] = ..., cmd_connect_ans_d6: _Optional[int] = ..., cmd_connect_ans_d5: _Optional[int] = ..., cmd_connect_ans_d4: _Optional[int] = ..., cmd_connect_ans_d3: _Optional[int] = ..., cmd_connect_ans_d2: _Optional[int] = ..., cmd_connect_ans_d1: _Optional[int] = ...) -> None: ...
