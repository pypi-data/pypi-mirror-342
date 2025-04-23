from make87_messages_ros2.rolling.py_trees_ros_interfaces.msg import publisher_details_pb2 as _publisher_details_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IntrospectPublishersRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class IntrospectPublishersResponse(_message.Message):
    __slots__ = ("publisher_details",)
    PUBLISHER_DETAILS_FIELD_NUMBER: _ClassVar[int]
    publisher_details: _containers.RepeatedCompositeFieldContainer[_publisher_details_pb2.PublisherDetails]
    def __init__(self, publisher_details: _Optional[_Iterable[_Union[_publisher_details_pb2.PublisherDetails, _Mapping]]] = ...) -> None: ...
