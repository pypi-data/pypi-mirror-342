from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.py_trees_ros_interfaces.msg import subscriber_details_pb2 as _subscriber_details_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IntrospectSubscribersRequest(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class IntrospectSubscribersResponse(_message.Message):
    __slots__ = ("header", "subscriber_details")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIBER_DETAILS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    subscriber_details: _containers.RepeatedCompositeFieldContainer[_subscriber_details_pb2.SubscriberDetails]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., subscriber_details: _Optional[_Iterable[_Union[_subscriber_details_pb2.SubscriberDetails, _Mapping]]] = ...) -> None: ...
