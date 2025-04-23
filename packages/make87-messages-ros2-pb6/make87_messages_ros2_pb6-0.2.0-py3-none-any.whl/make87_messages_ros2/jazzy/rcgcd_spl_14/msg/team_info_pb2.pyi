from make87_messages_ros2.jazzy.rcgcd_spl_14.msg import robot_info_pb2 as _robot_info_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TeamInfo(_message.Message):
    __slots__ = ("team_number", "team_colour", "score", "penalty_shot", "single_shots", "message_budget", "players")
    TEAM_NUMBER_FIELD_NUMBER: _ClassVar[int]
    TEAM_COLOUR_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    PENALTY_SHOT_FIELD_NUMBER: _ClassVar[int]
    SINGLE_SHOTS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_BUDGET_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    team_number: int
    team_colour: int
    score: int
    penalty_shot: int
    single_shots: int
    message_budget: int
    players: _containers.RepeatedCompositeFieldContainer[_robot_info_pb2.RobotInfo]
    def __init__(self, team_number: _Optional[int] = ..., team_colour: _Optional[int] = ..., score: _Optional[int] = ..., penalty_shot: _Optional[int] = ..., single_shots: _Optional[int] = ..., message_budget: _Optional[int] = ..., players: _Optional[_Iterable[_Union[_robot_info_pb2.RobotInfo, _Mapping]]] = ...) -> None: ...
