from make87_messages_ros2.jazzy.four_wheel_steering_msgs.msg import four_wheel_steering_pb2 as _four_wheel_steering_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FourWheelSteeringStamped(_message.Message):
    __slots__ = ("header", "data")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    data: _four_wheel_steering_pb2.FourWheelSteering
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., data: _Optional[_Union[_four_wheel_steering_pb2.FourWheelSteering, _Mapping]] = ...) -> None: ...
