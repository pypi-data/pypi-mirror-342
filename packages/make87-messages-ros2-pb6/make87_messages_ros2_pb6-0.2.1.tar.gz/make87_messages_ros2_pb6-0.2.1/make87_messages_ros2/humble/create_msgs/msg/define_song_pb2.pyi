from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DefineSong(_message.Message):
    __slots__ = ("header", "song", "length", "notes", "durations")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SONG_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    NOTES_FIELD_NUMBER: _ClassVar[int]
    DURATIONS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    song: int
    length: int
    notes: _containers.RepeatedScalarFieldContainer[int]
    durations: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., song: _Optional[int] = ..., length: _Optional[int] = ..., notes: _Optional[_Iterable[int]] = ..., durations: _Optional[_Iterable[float]] = ...) -> None: ...
