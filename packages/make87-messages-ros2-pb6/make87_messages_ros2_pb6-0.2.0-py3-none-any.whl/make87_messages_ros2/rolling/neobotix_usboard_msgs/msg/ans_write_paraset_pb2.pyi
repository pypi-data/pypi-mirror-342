from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AnsWriteParaset(_message.Message):
    __slots__ = ("header", "command", "paramset_cksum_low_byte", "paramset_cksum_high_byte")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    PARAMSET_CKSUM_LOW_BYTE_FIELD_NUMBER: _ClassVar[int]
    PARAMSET_CKSUM_HIGH_BYTE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    command: int
    paramset_cksum_low_byte: int
    paramset_cksum_high_byte: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., command: _Optional[int] = ..., paramset_cksum_low_byte: _Optional[int] = ..., paramset_cksum_high_byte: _Optional[int] = ...) -> None: ...
