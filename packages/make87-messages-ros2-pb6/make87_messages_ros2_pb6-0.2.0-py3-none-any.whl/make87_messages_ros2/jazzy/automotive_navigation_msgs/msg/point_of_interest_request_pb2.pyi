from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PointOfInterestRequest(_message.Message):
    __slots__ = ("header", "name", "module_name", "request_id", "cancel", "update_num", "guid_valid", "guid", "tolerance")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MODULE_NAME_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    CANCEL_FIELD_NUMBER: _ClassVar[int]
    UPDATE_NUM_FIELD_NUMBER: _ClassVar[int]
    GUID_VALID_FIELD_NUMBER: _ClassVar[int]
    GUID_FIELD_NUMBER: _ClassVar[int]
    TOLERANCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    module_name: str
    request_id: int
    cancel: int
    update_num: int
    guid_valid: int
    guid: int
    tolerance: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., module_name: _Optional[str] = ..., request_id: _Optional[int] = ..., cancel: _Optional[int] = ..., update_num: _Optional[int] = ..., guid_valid: _Optional[int] = ..., guid: _Optional[int] = ..., tolerance: _Optional[float] = ...) -> None: ...
