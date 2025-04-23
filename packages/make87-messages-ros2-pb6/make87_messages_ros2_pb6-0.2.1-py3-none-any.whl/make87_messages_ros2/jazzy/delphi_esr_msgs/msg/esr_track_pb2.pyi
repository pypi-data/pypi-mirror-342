from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EsrTrack(_message.Message):
    __slots__ = ("header", "canmsg", "id", "lat_rate", "grouping_changed", "oncoming", "status", "angle", "range", "bridge_object", "rolling_count", "width", "range_accel", "med_range_mode", "range_rate")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CANMSG_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    LAT_RATE_FIELD_NUMBER: _ClassVar[int]
    GROUPING_CHANGED_FIELD_NUMBER: _ClassVar[int]
    ONCOMING_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ANGLE_FIELD_NUMBER: _ClassVar[int]
    RANGE_FIELD_NUMBER: _ClassVar[int]
    BRIDGE_OBJECT_FIELD_NUMBER: _ClassVar[int]
    ROLLING_COUNT_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    RANGE_ACCEL_FIELD_NUMBER: _ClassVar[int]
    MED_RANGE_MODE_FIELD_NUMBER: _ClassVar[int]
    RANGE_RATE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    canmsg: str
    id: int
    lat_rate: float
    grouping_changed: bool
    oncoming: bool
    status: int
    angle: float
    range: float
    bridge_object: bool
    rolling_count: bool
    width: float
    range_accel: float
    med_range_mode: int
    range_rate: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., canmsg: _Optional[str] = ..., id: _Optional[int] = ..., lat_rate: _Optional[float] = ..., grouping_changed: bool = ..., oncoming: bool = ..., status: _Optional[int] = ..., angle: _Optional[float] = ..., range: _Optional[float] = ..., bridge_object: bool = ..., rolling_count: bool = ..., width: _Optional[float] = ..., range_accel: _Optional[float] = ..., med_range_mode: _Optional[int] = ..., range_rate: _Optional[float] = ...) -> None: ...
