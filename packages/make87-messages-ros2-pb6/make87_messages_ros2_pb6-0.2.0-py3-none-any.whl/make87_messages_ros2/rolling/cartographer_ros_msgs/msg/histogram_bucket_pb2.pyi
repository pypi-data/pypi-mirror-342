from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class HistogramBucket(_message.Message):
    __slots__ = ("bucket_boundary", "count")
    BUCKET_BOUNDARY_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    bucket_boundary: float
    count: float
    def __init__(self, bucket_boundary: _Optional[float] = ..., count: _Optional[float] = ...) -> None: ...
