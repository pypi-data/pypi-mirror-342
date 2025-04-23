from make87_messages_ros2.rolling.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IbeoDataHeader(_message.Message):
    __slots__ = ("previous_message_size", "message_size", "device_id", "data_type_id", "stamp")
    PREVIOUS_MESSAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_ID_FIELD_NUMBER: _ClassVar[int]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    previous_message_size: int
    message_size: int
    device_id: int
    data_type_id: int
    stamp: _time_pb2.Time
    def __init__(self, previous_message_size: _Optional[int] = ..., message_size: _Optional[int] = ..., device_id: _Optional[int] = ..., data_type_id: _Optional[int] = ..., stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ...) -> None: ...
