from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Frame64(_message.Message):
    __slots__ = ("header", "id", "extended", "fdf", "brs", "esi", "rtr", "size", "data")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    EXTENDED_FIELD_NUMBER: _ClassVar[int]
    FDF_FIELD_NUMBER: _ClassVar[int]
    BRS_FIELD_NUMBER: _ClassVar[int]
    ESI_FIELD_NUMBER: _ClassVar[int]
    RTR_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    id: int
    extended: bool
    fdf: bool
    brs: bool
    esi: bool
    rtr: bool
    size: int
    data: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., id: _Optional[int] = ..., extended: bool = ..., fdf: bool = ..., brs: bool = ..., esi: bool = ..., rtr: bool = ..., size: _Optional[int] = ..., data: _Optional[_Iterable[int]] = ...) -> None: ...
