from make87_messages_ros2.jazzy.std_msgs.msg import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClearCostmapExceptRegionRequest(_message.Message):
    __slots__ = ("reset_distance",)
    RESET_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    reset_distance: float
    def __init__(self, reset_distance: _Optional[float] = ...) -> None: ...

class ClearCostmapExceptRegionResponse(_message.Message):
    __slots__ = ("response",)
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: _empty_pb2.Empty
    def __init__(self, response: _Optional[_Union[_empty_pb2.Empty, _Mapping]] = ...) -> None: ...
