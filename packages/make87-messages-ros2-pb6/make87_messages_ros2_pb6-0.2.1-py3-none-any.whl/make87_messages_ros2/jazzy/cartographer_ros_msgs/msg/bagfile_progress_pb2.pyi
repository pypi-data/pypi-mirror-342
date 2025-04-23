from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BagfileProgress(_message.Message):
    __slots__ = ("current_bagfile_name", "current_bagfile_id", "total_bagfiles", "total_messages", "processed_messages", "total_seconds", "processed_seconds")
    CURRENT_BAGFILE_NAME_FIELD_NUMBER: _ClassVar[int]
    CURRENT_BAGFILE_ID_FIELD_NUMBER: _ClassVar[int]
    TOTAL_BAGFILES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    PROCESSED_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    PROCESSED_SECONDS_FIELD_NUMBER: _ClassVar[int]
    current_bagfile_name: str
    current_bagfile_id: int
    total_bagfiles: int
    total_messages: int
    processed_messages: int
    total_seconds: float
    processed_seconds: float
    def __init__(self, current_bagfile_name: _Optional[str] = ..., current_bagfile_id: _Optional[int] = ..., total_bagfiles: _Optional[int] = ..., total_messages: _Optional[int] = ..., processed_messages: _Optional[int] = ..., total_seconds: _Optional[float] = ..., processed_seconds: _Optional[float] = ...) -> None: ...
