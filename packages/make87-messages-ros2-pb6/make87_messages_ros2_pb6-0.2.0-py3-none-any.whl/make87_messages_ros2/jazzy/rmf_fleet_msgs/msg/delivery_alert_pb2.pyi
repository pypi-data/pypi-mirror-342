from make87_messages_ros2.jazzy.rmf_fleet_msgs.msg import delivery_alert_action_pb2 as _delivery_alert_action_pb2
from make87_messages_ros2.jazzy.rmf_fleet_msgs.msg import delivery_alert_category_pb2 as _delivery_alert_category_pb2
from make87_messages_ros2.jazzy.rmf_fleet_msgs.msg import delivery_alert_tier_pb2 as _delivery_alert_tier_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DeliveryAlert(_message.Message):
    __slots__ = ("id", "category", "tier", "task_id", "action", "message")
    ID_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    TIER_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    id: str
    category: _delivery_alert_category_pb2.DeliveryAlertCategory
    tier: _delivery_alert_tier_pb2.DeliveryAlertTier
    task_id: str
    action: _delivery_alert_action_pb2.DeliveryAlertAction
    message: str
    def __init__(self, id: _Optional[str] = ..., category: _Optional[_Union[_delivery_alert_category_pb2.DeliveryAlertCategory, _Mapping]] = ..., tier: _Optional[_Union[_delivery_alert_tier_pb2.DeliveryAlertTier, _Mapping]] = ..., task_id: _Optional[str] = ..., action: _Optional[_Union[_delivery_alert_action_pb2.DeliveryAlertAction, _Mapping]] = ..., message: _Optional[str] = ...) -> None: ...
