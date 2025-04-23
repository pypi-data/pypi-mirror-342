from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.ibeo_msgs.msg import point2_di_pb2 as _point2_di_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Object2270(_message.Message):
    __slots__ = ("header", "id", "age", "prediction_age", "relative_moment_of_measurement", "reference_point_location", "reference_point_position_x", "reference_point_position_y", "reference_point_position_sigma_x", "reference_point_position_sigma_y", "contour_points_cog_x", "contour_points_cog_y", "object_box_length", "object_box_width", "object_box_orientation_angle", "object_box_orientation_angle_sigma", "absolute_velocity_x", "absolute_velocity_y", "absolute_velocity_sigma_x", "absolute_velocity_sigma_y", "relative_velocity_x", "relative_velocity_y", "relative_velocity_sigma_x", "relative_velocity_sigma_y", "classification", "tracking_model", "mobile_detected", "track_valid", "classification_age", "classification_confidence", "number_of_contour_points", "contour_point_list")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    PREDICTION_AGE_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_MOMENT_OF_MEASUREMENT_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_POINT_LOCATION_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_POINT_POSITION_X_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_POINT_POSITION_Y_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_POINT_POSITION_SIGMA_X_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_POINT_POSITION_SIGMA_Y_FIELD_NUMBER: _ClassVar[int]
    CONTOUR_POINTS_COG_X_FIELD_NUMBER: _ClassVar[int]
    CONTOUR_POINTS_COG_Y_FIELD_NUMBER: _ClassVar[int]
    OBJECT_BOX_LENGTH_FIELD_NUMBER: _ClassVar[int]
    OBJECT_BOX_WIDTH_FIELD_NUMBER: _ClassVar[int]
    OBJECT_BOX_ORIENTATION_ANGLE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_BOX_ORIENTATION_ANGLE_SIGMA_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_VELOCITY_X_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_VELOCITY_Y_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_VELOCITY_SIGMA_X_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_VELOCITY_SIGMA_Y_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_VELOCITY_X_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_VELOCITY_Y_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_VELOCITY_SIGMA_X_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_VELOCITY_SIGMA_Y_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_FIELD_NUMBER: _ClassVar[int]
    TRACKING_MODEL_FIELD_NUMBER: _ClassVar[int]
    MOBILE_DETECTED_FIELD_NUMBER: _ClassVar[int]
    TRACK_VALID_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_AGE_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_CONTOUR_POINTS_FIELD_NUMBER: _ClassVar[int]
    CONTOUR_POINT_LIST_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    id: int
    age: int
    prediction_age: int
    relative_moment_of_measurement: int
    reference_point_location: int
    reference_point_position_x: int
    reference_point_position_y: int
    reference_point_position_sigma_x: int
    reference_point_position_sigma_y: int
    contour_points_cog_x: int
    contour_points_cog_y: int
    object_box_length: int
    object_box_width: int
    object_box_orientation_angle: int
    object_box_orientation_angle_sigma: int
    absolute_velocity_x: int
    absolute_velocity_y: int
    absolute_velocity_sigma_x: int
    absolute_velocity_sigma_y: int
    relative_velocity_x: int
    relative_velocity_y: int
    relative_velocity_sigma_x: int
    relative_velocity_sigma_y: int
    classification: int
    tracking_model: int
    mobile_detected: bool
    track_valid: bool
    classification_age: int
    classification_confidence: int
    number_of_contour_points: int
    contour_point_list: _containers.RepeatedCompositeFieldContainer[_point2_di_pb2.Point2Di]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., id: _Optional[int] = ..., age: _Optional[int] = ..., prediction_age: _Optional[int] = ..., relative_moment_of_measurement: _Optional[int] = ..., reference_point_location: _Optional[int] = ..., reference_point_position_x: _Optional[int] = ..., reference_point_position_y: _Optional[int] = ..., reference_point_position_sigma_x: _Optional[int] = ..., reference_point_position_sigma_y: _Optional[int] = ..., contour_points_cog_x: _Optional[int] = ..., contour_points_cog_y: _Optional[int] = ..., object_box_length: _Optional[int] = ..., object_box_width: _Optional[int] = ..., object_box_orientation_angle: _Optional[int] = ..., object_box_orientation_angle_sigma: _Optional[int] = ..., absolute_velocity_x: _Optional[int] = ..., absolute_velocity_y: _Optional[int] = ..., absolute_velocity_sigma_x: _Optional[int] = ..., absolute_velocity_sigma_y: _Optional[int] = ..., relative_velocity_x: _Optional[int] = ..., relative_velocity_y: _Optional[int] = ..., relative_velocity_sigma_x: _Optional[int] = ..., relative_velocity_sigma_y: _Optional[int] = ..., classification: _Optional[int] = ..., tracking_model: _Optional[int] = ..., mobile_detected: bool = ..., track_valid: bool = ..., classification_age: _Optional[int] = ..., classification_confidence: _Optional[int] = ..., number_of_contour_points: _Optional[int] = ..., contour_point_list: _Optional[_Iterable[_Union[_point2_di_pb2.Point2Di, _Mapping]]] = ...) -> None: ...
