from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.cob_msgs.msg import emergency_stop_state_pb2 as _emergency_stop_state_pb2
from make87_messages_ros2.humble.cob_msgs.msg import power_state_pb2 as _power_state_pb2
from make87_messages_ros2.humble.diagnostic_msgs.msg import diagnostic_status_pb2 as _diagnostic_status_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DashboardState(_message.Message):
    __slots__ = ("header", "diagnostics_toplevel_state", "power_state", "emergency_stop_state")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DIAGNOSTICS_TOPLEVEL_STATE_FIELD_NUMBER: _ClassVar[int]
    POWER_STATE_FIELD_NUMBER: _ClassVar[int]
    EMERGENCY_STOP_STATE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    diagnostics_toplevel_state: _diagnostic_status_pb2.DiagnosticStatus
    power_state: _power_state_pb2.PowerState
    emergency_stop_state: _emergency_stop_state_pb2.EmergencyStopState
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., diagnostics_toplevel_state: _Optional[_Union[_diagnostic_status_pb2.DiagnosticStatus, _Mapping]] = ..., power_state: _Optional[_Union[_power_state_pb2.PowerState, _Mapping]] = ..., emergency_stop_state: _Optional[_Union[_emergency_stop_state_pb2.EmergencyStopState, _Mapping]] = ...) -> None: ...
