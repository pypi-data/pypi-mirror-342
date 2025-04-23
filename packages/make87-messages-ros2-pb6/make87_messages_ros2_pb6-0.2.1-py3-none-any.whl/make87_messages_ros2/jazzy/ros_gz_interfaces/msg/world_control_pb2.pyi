from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.jazzy.ros_gz_interfaces.msg import world_reset_pb2 as _world_reset_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WorldControl(_message.Message):
    __slots__ = ("pause", "step", "multi_step", "reset", "seed", "run_to_sim_time")
    PAUSE_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    MULTI_STEP_FIELD_NUMBER: _ClassVar[int]
    RESET_FIELD_NUMBER: _ClassVar[int]
    SEED_FIELD_NUMBER: _ClassVar[int]
    RUN_TO_SIM_TIME_FIELD_NUMBER: _ClassVar[int]
    pause: bool
    step: bool
    multi_step: int
    reset: _world_reset_pb2.WorldReset
    seed: int
    run_to_sim_time: _time_pb2.Time
    def __init__(self, pause: bool = ..., step: bool = ..., multi_step: _Optional[int] = ..., reset: _Optional[_Union[_world_reset_pb2.WorldReset, _Mapping]] = ..., seed: _Optional[int] = ..., run_to_sim_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ...) -> None: ...
