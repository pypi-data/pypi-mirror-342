from make87_messages_ros2.rolling.rmf_traffic_msgs.msg import schedule_identity_pb2 as _schedule_identity_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RequestChangesRequest(_message.Message):
    __slots__ = ("query_id", "version", "full_update")
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    FULL_UPDATE_FIELD_NUMBER: _ClassVar[int]
    query_id: int
    version: int
    full_update: bool
    def __init__(self, query_id: _Optional[int] = ..., version: _Optional[int] = ..., full_update: bool = ...) -> None: ...

class RequestChangesResponse(_message.Message):
    __slots__ = ("node_id", "result", "error")
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    node_id: _schedule_identity_pb2.ScheduleIdentity
    result: int
    error: str
    def __init__(self, node_id: _Optional[_Union[_schedule_identity_pb2.ScheduleIdentity, _Mapping]] = ..., result: _Optional[int] = ..., error: _Optional[str] = ...) -> None: ...
