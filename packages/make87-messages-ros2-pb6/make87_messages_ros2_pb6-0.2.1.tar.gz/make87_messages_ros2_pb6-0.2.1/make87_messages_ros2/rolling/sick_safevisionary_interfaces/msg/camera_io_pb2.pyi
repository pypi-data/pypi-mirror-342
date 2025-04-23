from make87_messages_ros2.rolling.sick_safevisionary_interfaces.msg import io_configured_pb2 as _io_configured_pb2
from make87_messages_ros2.rolling.sick_safevisionary_interfaces.msg import io_direction_pb2 as _io_direction_pb2
from make87_messages_ros2.rolling.sick_safevisionary_interfaces.msg import io_input_values_pb2 as _io_input_values_pb2
from make87_messages_ros2.rolling.sick_safevisionary_interfaces.msg import io_output_values_pb2 as _io_output_values_pb2
from make87_messages_ros2.rolling.sick_safevisionary_interfaces.msg import ioossds_state_pb2 as _ioossds_state_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CameraIO(_message.Message):
    __slots__ = ("header", "configured", "direction", "input_values", "output_values", "ossds_state", "ossds_dyn_count", "ossds_crc", "ossds_io_status", "dynamic_speed_a", "dynamic_speed_b", "dynamic_valid_flags")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CONFIGURED_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    INPUT_VALUES_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_VALUES_FIELD_NUMBER: _ClassVar[int]
    OSSDS_STATE_FIELD_NUMBER: _ClassVar[int]
    OSSDS_DYN_COUNT_FIELD_NUMBER: _ClassVar[int]
    OSSDS_CRC_FIELD_NUMBER: _ClassVar[int]
    OSSDS_IO_STATUS_FIELD_NUMBER: _ClassVar[int]
    DYNAMIC_SPEED_A_FIELD_NUMBER: _ClassVar[int]
    DYNAMIC_SPEED_B_FIELD_NUMBER: _ClassVar[int]
    DYNAMIC_VALID_FLAGS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    configured: _io_configured_pb2.IOConfigured
    direction: _io_direction_pb2.IODirection
    input_values: _io_input_values_pb2.IOInputValues
    output_values: _io_output_values_pb2.IOOutputValues
    ossds_state: _ioossds_state_pb2.IOOSSDSState
    ossds_dyn_count: int
    ossds_crc: int
    ossds_io_status: int
    dynamic_speed_a: int
    dynamic_speed_b: int
    dynamic_valid_flags: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., configured: _Optional[_Union[_io_configured_pb2.IOConfigured, _Mapping]] = ..., direction: _Optional[_Union[_io_direction_pb2.IODirection, _Mapping]] = ..., input_values: _Optional[_Union[_io_input_values_pb2.IOInputValues, _Mapping]] = ..., output_values: _Optional[_Union[_io_output_values_pb2.IOOutputValues, _Mapping]] = ..., ossds_state: _Optional[_Union[_ioossds_state_pb2.IOOSSDSState, _Mapping]] = ..., ossds_dyn_count: _Optional[int] = ..., ossds_crc: _Optional[int] = ..., ossds_io_status: _Optional[int] = ..., dynamic_speed_a: _Optional[int] = ..., dynamic_speed_b: _Optional[int] = ..., dynamic_valid_flags: _Optional[int] = ...) -> None: ...
