from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NewMqtt2RosBridgeRequest(_message.Message):
    __slots__ = ("header", "ros_topic", "mqtt_topic", "primitive", "mqtt_qos", "ros_queue_size", "ros_latched")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS_TOPIC_FIELD_NUMBER: _ClassVar[int]
    MQTT_TOPIC_FIELD_NUMBER: _ClassVar[int]
    PRIMITIVE_FIELD_NUMBER: _ClassVar[int]
    MQTT_QOS_FIELD_NUMBER: _ClassVar[int]
    ROS_QUEUE_SIZE_FIELD_NUMBER: _ClassVar[int]
    ROS_LATCHED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros_topic: str
    mqtt_topic: str
    primitive: bool
    mqtt_qos: int
    ros_queue_size: int
    ros_latched: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros_topic: _Optional[str] = ..., mqtt_topic: _Optional[str] = ..., primitive: bool = ..., mqtt_qos: _Optional[int] = ..., ros_queue_size: _Optional[int] = ..., ros_latched: bool = ...) -> None: ...

class NewMqtt2RosBridgeResponse(_message.Message):
    __slots__ = ("header", "success")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ...) -> None: ...
