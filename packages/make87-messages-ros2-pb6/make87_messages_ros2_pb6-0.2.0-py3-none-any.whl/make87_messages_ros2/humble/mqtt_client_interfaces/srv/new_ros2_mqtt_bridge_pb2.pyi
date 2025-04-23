from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NewRos2MqttBridgeRequest(_message.Message):
    __slots__ = ("header", "ros_topic", "mqtt_topic", "primitive", "inject_timestamp", "ros_queue_size", "mqtt_qos", "mqtt_retained")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS_TOPIC_FIELD_NUMBER: _ClassVar[int]
    MQTT_TOPIC_FIELD_NUMBER: _ClassVar[int]
    PRIMITIVE_FIELD_NUMBER: _ClassVar[int]
    INJECT_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ROS_QUEUE_SIZE_FIELD_NUMBER: _ClassVar[int]
    MQTT_QOS_FIELD_NUMBER: _ClassVar[int]
    MQTT_RETAINED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros_topic: str
    mqtt_topic: str
    primitive: bool
    inject_timestamp: bool
    ros_queue_size: int
    mqtt_qos: int
    mqtt_retained: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros_topic: _Optional[str] = ..., mqtt_topic: _Optional[str] = ..., primitive: bool = ..., inject_timestamp: bool = ..., ros_queue_size: _Optional[int] = ..., mqtt_qos: _Optional[int] = ..., mqtt_retained: bool = ...) -> None: ...

class NewRos2MqttBridgeResponse(_message.Message):
    __slots__ = ("header", "success")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ...) -> None: ...
