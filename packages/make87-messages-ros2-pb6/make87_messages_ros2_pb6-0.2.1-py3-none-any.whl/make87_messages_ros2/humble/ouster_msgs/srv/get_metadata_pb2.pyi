from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.ouster_msgs.msg import metadata_pb2 as _metadata_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetMetadataRequest(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class GetMetadataResponse(_message.Message):
    __slots__ = ("header", "metadata")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    metadata: _metadata_pb2.Metadata
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., metadata: _Optional[_Union[_metadata_pb2.Metadata, _Mapping]] = ...) -> None: ...
