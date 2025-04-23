from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IntegerRange(_message.Message):
    __slots__ = ("header", "from_value", "to_value", "step")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FROM_VALUE_FIELD_NUMBER: _ClassVar[int]
    TO_VALUE_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    from_value: int
    to_value: int
    step: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., from_value: _Optional[int] = ..., to_value: _Optional[int] = ..., step: _Optional[int] = ...) -> None: ...
