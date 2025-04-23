from make87_messages_ros2.rolling.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LiftState(_message.Message):
    __slots__ = ("lift_time", "lift_name", "available_floors", "current_floor", "destination_floor", "door_state", "motion_state", "available_modes", "current_mode", "session_id")
    LIFT_TIME_FIELD_NUMBER: _ClassVar[int]
    LIFT_NAME_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_FLOORS_FIELD_NUMBER: _ClassVar[int]
    CURRENT_FLOOR_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_FLOOR_FIELD_NUMBER: _ClassVar[int]
    DOOR_STATE_FIELD_NUMBER: _ClassVar[int]
    MOTION_STATE_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_MODES_FIELD_NUMBER: _ClassVar[int]
    CURRENT_MODE_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    lift_time: _time_pb2.Time
    lift_name: str
    available_floors: _containers.RepeatedScalarFieldContainer[str]
    current_floor: str
    destination_floor: str
    door_state: int
    motion_state: int
    available_modes: _containers.RepeatedScalarFieldContainer[int]
    current_mode: int
    session_id: str
    def __init__(self, lift_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., lift_name: _Optional[str] = ..., available_floors: _Optional[_Iterable[str]] = ..., current_floor: _Optional[str] = ..., destination_floor: _Optional[str] = ..., door_state: _Optional[int] = ..., motion_state: _Optional[int] = ..., available_modes: _Optional[_Iterable[int]] = ..., current_mode: _Optional[int] = ..., session_id: _Optional[str] = ...) -> None: ...
