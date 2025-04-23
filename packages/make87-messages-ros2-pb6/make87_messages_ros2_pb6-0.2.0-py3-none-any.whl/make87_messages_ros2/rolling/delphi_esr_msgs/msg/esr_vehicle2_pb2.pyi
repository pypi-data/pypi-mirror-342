from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EsrVehicle2(_message.Message):
    __slots__ = ("header", "scan_index_ack", "use_angle_misalignment", "clear_faults", "high_yaw_angle", "mr_only_transmit", "lr_only_transmit", "angle_misalignment", "lateral_mounting_offset", "radar_cmd_radiate", "blockage_disable", "maximum_tracks", "turn_signal_status", "vehicle_speed_validity", "mmr_upside_down", "grouping_mode", "wiper_status", "raw_data_enable")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SCAN_INDEX_ACK_FIELD_NUMBER: _ClassVar[int]
    USE_ANGLE_MISALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    CLEAR_FAULTS_FIELD_NUMBER: _ClassVar[int]
    HIGH_YAW_ANGLE_FIELD_NUMBER: _ClassVar[int]
    MR_ONLY_TRANSMIT_FIELD_NUMBER: _ClassVar[int]
    LR_ONLY_TRANSMIT_FIELD_NUMBER: _ClassVar[int]
    ANGLE_MISALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    LATERAL_MOUNTING_OFFSET_FIELD_NUMBER: _ClassVar[int]
    RADAR_CMD_RADIATE_FIELD_NUMBER: _ClassVar[int]
    BLOCKAGE_DISABLE_FIELD_NUMBER: _ClassVar[int]
    MAXIMUM_TRACKS_FIELD_NUMBER: _ClassVar[int]
    TURN_SIGNAL_STATUS_FIELD_NUMBER: _ClassVar[int]
    VEHICLE_SPEED_VALIDITY_FIELD_NUMBER: _ClassVar[int]
    MMR_UPSIDE_DOWN_FIELD_NUMBER: _ClassVar[int]
    GROUPING_MODE_FIELD_NUMBER: _ClassVar[int]
    WIPER_STATUS_FIELD_NUMBER: _ClassVar[int]
    RAW_DATA_ENABLE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    scan_index_ack: int
    use_angle_misalignment: bool
    clear_faults: bool
    high_yaw_angle: int
    mr_only_transmit: bool
    lr_only_transmit: bool
    angle_misalignment: float
    lateral_mounting_offset: float
    radar_cmd_radiate: bool
    blockage_disable: bool
    maximum_tracks: int
    turn_signal_status: int
    vehicle_speed_validity: bool
    mmr_upside_down: bool
    grouping_mode: int
    wiper_status: bool
    raw_data_enable: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., scan_index_ack: _Optional[int] = ..., use_angle_misalignment: bool = ..., clear_faults: bool = ..., high_yaw_angle: _Optional[int] = ..., mr_only_transmit: bool = ..., lr_only_transmit: bool = ..., angle_misalignment: _Optional[float] = ..., lateral_mounting_offset: _Optional[float] = ..., radar_cmd_radiate: bool = ..., blockage_disable: bool = ..., maximum_tracks: _Optional[int] = ..., turn_signal_status: _Optional[int] = ..., vehicle_speed_validity: bool = ..., mmr_upside_down: bool = ..., grouping_mode: _Optional[int] = ..., wiper_status: bool = ..., raw_data_enable: bool = ...) -> None: ...
