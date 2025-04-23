from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UBXNavPosLLH(_message.Message):
    __slots__ = ("header", "itow", "lon", "lat", "height", "hmsl", "h_acc", "v_acc")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ITOW_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    HMSL_FIELD_NUMBER: _ClassVar[int]
    H_ACC_FIELD_NUMBER: _ClassVar[int]
    V_ACC_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    itow: int
    lon: int
    lat: int
    height: int
    hmsl: int
    h_acc: int
    v_acc: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., itow: _Optional[int] = ..., lon: _Optional[int] = ..., lat: _Optional[int] = ..., height: _Optional[int] = ..., hmsl: _Optional[int] = ..., h_acc: _Optional[int] = ..., v_acc: _Optional[int] = ...) -> None: ...
