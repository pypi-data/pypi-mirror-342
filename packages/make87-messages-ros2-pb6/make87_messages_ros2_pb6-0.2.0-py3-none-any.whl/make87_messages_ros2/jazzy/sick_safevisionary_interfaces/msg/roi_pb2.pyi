from make87_messages_ros2.jazzy.sick_safevisionary_interfaces.msg import roi_observation_result_data_pb2 as _roi_observation_result_data_pb2
from make87_messages_ros2.jazzy.sick_safevisionary_interfaces.msg import roi_observation_safety_data_pb2 as _roi_observation_safety_data_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ROI(_message.Message):
    __slots__ = ("id", "result_data", "safety_data", "distance_value")
    ID_FIELD_NUMBER: _ClassVar[int]
    RESULT_DATA_FIELD_NUMBER: _ClassVar[int]
    SAFETY_DATA_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_VALUE_FIELD_NUMBER: _ClassVar[int]
    id: int
    result_data: _roi_observation_result_data_pb2.ROIObservationResultData
    safety_data: _roi_observation_safety_data_pb2.ROIObservationSafetyData
    distance_value: int
    def __init__(self, id: _Optional[int] = ..., result_data: _Optional[_Union[_roi_observation_result_data_pb2.ROIObservationResultData, _Mapping]] = ..., safety_data: _Optional[_Union[_roi_observation_safety_data_pb2.ROIObservationSafetyData, _Mapping]] = ..., distance_value: _Optional[int] = ...) -> None: ...
