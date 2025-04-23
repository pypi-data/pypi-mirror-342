from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SaveMapRequest(_message.Message):
    __slots__ = ("header", "map_topic", "map_url", "image_format", "map_mode", "free_thresh", "occupied_thresh")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MAP_TOPIC_FIELD_NUMBER: _ClassVar[int]
    MAP_URL_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FORMAT_FIELD_NUMBER: _ClassVar[int]
    MAP_MODE_FIELD_NUMBER: _ClassVar[int]
    FREE_THRESH_FIELD_NUMBER: _ClassVar[int]
    OCCUPIED_THRESH_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    map_topic: str
    map_url: str
    image_format: str
    map_mode: str
    free_thresh: float
    occupied_thresh: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., map_topic: _Optional[str] = ..., map_url: _Optional[str] = ..., image_format: _Optional[str] = ..., map_mode: _Optional[str] = ..., free_thresh: _Optional[float] = ..., occupied_thresh: _Optional[float] = ...) -> None: ...

class SaveMapResponse(_message.Message):
    __slots__ = ("header", "result")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    result: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., result: bool = ...) -> None: ...
