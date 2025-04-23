from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ResourceUsageReport(_message.Message):
    __slots__ = ("header", "pid", "cpu_cores_utilized", "total_memory_bytes", "free_memory_bytes", "process_memory_bytes")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PID_FIELD_NUMBER: _ClassVar[int]
    CPU_CORES_UTILIZED_FIELD_NUMBER: _ClassVar[int]
    TOTAL_MEMORY_BYTES_FIELD_NUMBER: _ClassVar[int]
    FREE_MEMORY_BYTES_FIELD_NUMBER: _ClassVar[int]
    PROCESS_MEMORY_BYTES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    pid: int
    cpu_cores_utilized: float
    total_memory_bytes: int
    free_memory_bytes: int
    process_memory_bytes: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., pid: _Optional[int] = ..., cpu_cores_utilized: _Optional[float] = ..., total_memory_bytes: _Optional[int] = ..., free_memory_bytes: _Optional[int] = ..., process_memory_bytes: _Optional[int] = ...) -> None: ...
