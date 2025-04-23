from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CabinReport(_message.Message):
    __slots__ = ("header", "door_open_front_right", "door_open_front_left", "door_open_rear_right", "door_open_rear_left", "hood_open", "trunk_open", "passenger_present", "passenger_airbag_enabled", "seatbelt_engaged_driver", "seatbelt_engaged_passenger")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DOOR_OPEN_FRONT_RIGHT_FIELD_NUMBER: _ClassVar[int]
    DOOR_OPEN_FRONT_LEFT_FIELD_NUMBER: _ClassVar[int]
    DOOR_OPEN_REAR_RIGHT_FIELD_NUMBER: _ClassVar[int]
    DOOR_OPEN_REAR_LEFT_FIELD_NUMBER: _ClassVar[int]
    HOOD_OPEN_FIELD_NUMBER: _ClassVar[int]
    TRUNK_OPEN_FIELD_NUMBER: _ClassVar[int]
    PASSENGER_PRESENT_FIELD_NUMBER: _ClassVar[int]
    PASSENGER_AIRBAG_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SEATBELT_ENGAGED_DRIVER_FIELD_NUMBER: _ClassVar[int]
    SEATBELT_ENGAGED_PASSENGER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    door_open_front_right: bool
    door_open_front_left: bool
    door_open_rear_right: bool
    door_open_rear_left: bool
    hood_open: bool
    trunk_open: bool
    passenger_present: bool
    passenger_airbag_enabled: bool
    seatbelt_engaged_driver: bool
    seatbelt_engaged_passenger: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., door_open_front_right: bool = ..., door_open_front_left: bool = ..., door_open_rear_right: bool = ..., door_open_rear_left: bool = ..., hood_open: bool = ..., trunk_open: bool = ..., passenger_present: bool = ..., passenger_airbag_enabled: bool = ..., seatbelt_engaged_driver: bool = ..., seatbelt_engaged_passenger: bool = ...) -> None: ...
