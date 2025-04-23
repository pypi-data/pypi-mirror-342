from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_dispenser_msgs.msg import dispenser_request_item_pb2 as _dispenser_request_item_pb2
from make87_messages_ros2.humble.rmf_task_msgs.msg import behavior_pb2 as _behavior_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Delivery(_message.Message):
    __slots__ = ("header", "task_id", "items", "pickup_place_name", "pickup_dispenser", "pickup_behavior", "dropoff_place_name", "dropoff_ingestor", "dropoff_behavior")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    PICKUP_PLACE_NAME_FIELD_NUMBER: _ClassVar[int]
    PICKUP_DISPENSER_FIELD_NUMBER: _ClassVar[int]
    PICKUP_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    DROPOFF_PLACE_NAME_FIELD_NUMBER: _ClassVar[int]
    DROPOFF_INGESTOR_FIELD_NUMBER: _ClassVar[int]
    DROPOFF_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    task_id: str
    items: _containers.RepeatedCompositeFieldContainer[_dispenser_request_item_pb2.DispenserRequestItem]
    pickup_place_name: str
    pickup_dispenser: str
    pickup_behavior: _behavior_pb2.Behavior
    dropoff_place_name: str
    dropoff_ingestor: str
    dropoff_behavior: _behavior_pb2.Behavior
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., task_id: _Optional[str] = ..., items: _Optional[_Iterable[_Union[_dispenser_request_item_pb2.DispenserRequestItem, _Mapping]]] = ..., pickup_place_name: _Optional[str] = ..., pickup_dispenser: _Optional[str] = ..., pickup_behavior: _Optional[_Union[_behavior_pb2.Behavior, _Mapping]] = ..., dropoff_place_name: _Optional[str] = ..., dropoff_ingestor: _Optional[str] = ..., dropoff_behavior: _Optional[_Union[_behavior_pb2.Behavior, _Mapping]] = ...) -> None: ...
