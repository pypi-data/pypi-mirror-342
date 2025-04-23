from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.flexbe_msgs.msg import outcome_condition_pb2 as _outcome_condition_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StateInstantiation(_message.Message):
    __slots__ = ("header", "state_path", "state_class", "initial_state_name", "input_keys", "output_keys", "cond_outcome", "cond_transition", "behavior_class", "parameter_names", "parameter_values", "position", "outcomes", "transitions", "autonomy", "userdata_keys", "userdata_remapping")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STATE_PATH_FIELD_NUMBER: _ClassVar[int]
    STATE_CLASS_FIELD_NUMBER: _ClassVar[int]
    INITIAL_STATE_NAME_FIELD_NUMBER: _ClassVar[int]
    INPUT_KEYS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_KEYS_FIELD_NUMBER: _ClassVar[int]
    COND_OUTCOME_FIELD_NUMBER: _ClassVar[int]
    COND_TRANSITION_FIELD_NUMBER: _ClassVar[int]
    BEHAVIOR_CLASS_FIELD_NUMBER: _ClassVar[int]
    PARAMETER_NAMES_FIELD_NUMBER: _ClassVar[int]
    PARAMETER_VALUES_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    OUTCOMES_FIELD_NUMBER: _ClassVar[int]
    TRANSITIONS_FIELD_NUMBER: _ClassVar[int]
    AUTONOMY_FIELD_NUMBER: _ClassVar[int]
    USERDATA_KEYS_FIELD_NUMBER: _ClassVar[int]
    USERDATA_REMAPPING_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    state_path: str
    state_class: str
    initial_state_name: str
    input_keys: _containers.RepeatedScalarFieldContainer[str]
    output_keys: _containers.RepeatedScalarFieldContainer[str]
    cond_outcome: _containers.RepeatedScalarFieldContainer[str]
    cond_transition: _containers.RepeatedCompositeFieldContainer[_outcome_condition_pb2.OutcomeCondition]
    behavior_class: str
    parameter_names: _containers.RepeatedScalarFieldContainer[str]
    parameter_values: _containers.RepeatedScalarFieldContainer[str]
    position: _containers.RepeatedScalarFieldContainer[float]
    outcomes: _containers.RepeatedScalarFieldContainer[str]
    transitions: _containers.RepeatedScalarFieldContainer[str]
    autonomy: _containers.RepeatedScalarFieldContainer[int]
    userdata_keys: _containers.RepeatedScalarFieldContainer[str]
    userdata_remapping: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., state_path: _Optional[str] = ..., state_class: _Optional[str] = ..., initial_state_name: _Optional[str] = ..., input_keys: _Optional[_Iterable[str]] = ..., output_keys: _Optional[_Iterable[str]] = ..., cond_outcome: _Optional[_Iterable[str]] = ..., cond_transition: _Optional[_Iterable[_Union[_outcome_condition_pb2.OutcomeCondition, _Mapping]]] = ..., behavior_class: _Optional[str] = ..., parameter_names: _Optional[_Iterable[str]] = ..., parameter_values: _Optional[_Iterable[str]] = ..., position: _Optional[_Iterable[float]] = ..., outcomes: _Optional[_Iterable[str]] = ..., transitions: _Optional[_Iterable[str]] = ..., autonomy: _Optional[_Iterable[int]] = ..., userdata_keys: _Optional[_Iterable[str]] = ..., userdata_remapping: _Optional[_Iterable[str]] = ...) -> None: ...
