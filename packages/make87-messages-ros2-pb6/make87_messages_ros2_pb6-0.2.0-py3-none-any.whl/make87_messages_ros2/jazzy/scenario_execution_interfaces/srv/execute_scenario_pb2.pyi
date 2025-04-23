from make87_messages_ros2.jazzy.scenario_execution_interfaces.msg import scenario_pb2 as _scenario_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ExecuteScenarioRequest(_message.Message):
    __slots__ = ("scenario",)
    SCENARIO_FIELD_NUMBER: _ClassVar[int]
    scenario: _scenario_pb2.Scenario
    def __init__(self, scenario: _Optional[_Union[_scenario_pb2.Scenario, _Mapping]] = ...) -> None: ...

class ExecuteScenarioResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: bool
    def __init__(self, result: bool = ...) -> None: ...
