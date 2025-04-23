from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RobotStateRTMsg(_message.Message):
    __slots__ = ("time", "q_target", "qd_target", "qdd_target", "i_target", "m_target", "q_actual", "qd_actual", "i_actual", "tool_acc_values", "tcp_force", "tool_vector", "tcp_speed", "digital_input_bits", "motor_temperatures", "controller_timer", "test_value", "robot_mode", "joint_modes")
    TIME_FIELD_NUMBER: _ClassVar[int]
    Q_TARGET_FIELD_NUMBER: _ClassVar[int]
    QD_TARGET_FIELD_NUMBER: _ClassVar[int]
    QDD_TARGET_FIELD_NUMBER: _ClassVar[int]
    I_TARGET_FIELD_NUMBER: _ClassVar[int]
    M_TARGET_FIELD_NUMBER: _ClassVar[int]
    Q_ACTUAL_FIELD_NUMBER: _ClassVar[int]
    QD_ACTUAL_FIELD_NUMBER: _ClassVar[int]
    I_ACTUAL_FIELD_NUMBER: _ClassVar[int]
    TOOL_ACC_VALUES_FIELD_NUMBER: _ClassVar[int]
    TCP_FORCE_FIELD_NUMBER: _ClassVar[int]
    TOOL_VECTOR_FIELD_NUMBER: _ClassVar[int]
    TCP_SPEED_FIELD_NUMBER: _ClassVar[int]
    DIGITAL_INPUT_BITS_FIELD_NUMBER: _ClassVar[int]
    MOTOR_TEMPERATURES_FIELD_NUMBER: _ClassVar[int]
    CONTROLLER_TIMER_FIELD_NUMBER: _ClassVar[int]
    TEST_VALUE_FIELD_NUMBER: _ClassVar[int]
    ROBOT_MODE_FIELD_NUMBER: _ClassVar[int]
    JOINT_MODES_FIELD_NUMBER: _ClassVar[int]
    time: float
    q_target: _containers.RepeatedScalarFieldContainer[float]
    qd_target: _containers.RepeatedScalarFieldContainer[float]
    qdd_target: _containers.RepeatedScalarFieldContainer[float]
    i_target: _containers.RepeatedScalarFieldContainer[float]
    m_target: _containers.RepeatedScalarFieldContainer[float]
    q_actual: _containers.RepeatedScalarFieldContainer[float]
    qd_actual: _containers.RepeatedScalarFieldContainer[float]
    i_actual: _containers.RepeatedScalarFieldContainer[float]
    tool_acc_values: _containers.RepeatedScalarFieldContainer[float]
    tcp_force: _containers.RepeatedScalarFieldContainer[float]
    tool_vector: _containers.RepeatedScalarFieldContainer[float]
    tcp_speed: _containers.RepeatedScalarFieldContainer[float]
    digital_input_bits: float
    motor_temperatures: _containers.RepeatedScalarFieldContainer[float]
    controller_timer: float
    test_value: float
    robot_mode: float
    joint_modes: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, time: _Optional[float] = ..., q_target: _Optional[_Iterable[float]] = ..., qd_target: _Optional[_Iterable[float]] = ..., qdd_target: _Optional[_Iterable[float]] = ..., i_target: _Optional[_Iterable[float]] = ..., m_target: _Optional[_Iterable[float]] = ..., q_actual: _Optional[_Iterable[float]] = ..., qd_actual: _Optional[_Iterable[float]] = ..., i_actual: _Optional[_Iterable[float]] = ..., tool_acc_values: _Optional[_Iterable[float]] = ..., tcp_force: _Optional[_Iterable[float]] = ..., tool_vector: _Optional[_Iterable[float]] = ..., tcp_speed: _Optional[_Iterable[float]] = ..., digital_input_bits: _Optional[float] = ..., motor_temperatures: _Optional[_Iterable[float]] = ..., controller_timer: _Optional[float] = ..., test_value: _Optional[float] = ..., robot_mode: _Optional[float] = ..., joint_modes: _Optional[_Iterable[float]] = ...) -> None: ...
