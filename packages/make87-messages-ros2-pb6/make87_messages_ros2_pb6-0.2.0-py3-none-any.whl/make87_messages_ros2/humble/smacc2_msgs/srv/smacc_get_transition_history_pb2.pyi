from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.smacc2_msgs.msg import smacc_transition_log_entry_pb2 as _smacc_transition_log_entry_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SmaccGetTransitionHistoryRequest(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class SmaccGetTransitionHistoryResponse(_message.Message):
    __slots__ = ("header", "history")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    HISTORY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    history: _containers.RepeatedCompositeFieldContainer[_smacc_transition_log_entry_pb2.SmaccTransitionLogEntry]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., history: _Optional[_Iterable[_Union[_smacc_transition_log_entry_pb2.SmaccTransitionLogEntry, _Mapping]]] = ...) -> None: ...
