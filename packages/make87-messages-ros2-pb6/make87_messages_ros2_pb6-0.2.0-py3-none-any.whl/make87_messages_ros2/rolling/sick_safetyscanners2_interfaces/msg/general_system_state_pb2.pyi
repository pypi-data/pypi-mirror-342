from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GeneralSystemState(_message.Message):
    __slots__ = ("run_mode_active", "standby_mode_active", "contamination_warning", "contamination_error", "reference_contour_status", "manipulation_status", "safe_cut_off_path", "non_safe_cut_off_path", "reset_required_cut_off_path", "current_monitoring_case_no_table_1", "current_monitoring_case_no_table_2", "current_monitoring_case_no_table_3", "current_monitoring_case_no_table_4", "application_error", "device_error")
    RUN_MODE_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    STANDBY_MODE_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    CONTAMINATION_WARNING_FIELD_NUMBER: _ClassVar[int]
    CONTAMINATION_ERROR_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_CONTOUR_STATUS_FIELD_NUMBER: _ClassVar[int]
    MANIPULATION_STATUS_FIELD_NUMBER: _ClassVar[int]
    SAFE_CUT_OFF_PATH_FIELD_NUMBER: _ClassVar[int]
    NON_SAFE_CUT_OFF_PATH_FIELD_NUMBER: _ClassVar[int]
    RESET_REQUIRED_CUT_OFF_PATH_FIELD_NUMBER: _ClassVar[int]
    CURRENT_MONITORING_CASE_NO_TABLE_1_FIELD_NUMBER: _ClassVar[int]
    CURRENT_MONITORING_CASE_NO_TABLE_2_FIELD_NUMBER: _ClassVar[int]
    CURRENT_MONITORING_CASE_NO_TABLE_3_FIELD_NUMBER: _ClassVar[int]
    CURRENT_MONITORING_CASE_NO_TABLE_4_FIELD_NUMBER: _ClassVar[int]
    APPLICATION_ERROR_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ERROR_FIELD_NUMBER: _ClassVar[int]
    run_mode_active: bool
    standby_mode_active: bool
    contamination_warning: bool
    contamination_error: bool
    reference_contour_status: bool
    manipulation_status: bool
    safe_cut_off_path: _containers.RepeatedScalarFieldContainer[bool]
    non_safe_cut_off_path: _containers.RepeatedScalarFieldContainer[bool]
    reset_required_cut_off_path: _containers.RepeatedScalarFieldContainer[bool]
    current_monitoring_case_no_table_1: int
    current_monitoring_case_no_table_2: int
    current_monitoring_case_no_table_3: int
    current_monitoring_case_no_table_4: int
    application_error: bool
    device_error: bool
    def __init__(self, run_mode_active: bool = ..., standby_mode_active: bool = ..., contamination_warning: bool = ..., contamination_error: bool = ..., reference_contour_status: bool = ..., manipulation_status: bool = ..., safe_cut_off_path: _Optional[_Iterable[bool]] = ..., non_safe_cut_off_path: _Optional[_Iterable[bool]] = ..., reset_required_cut_off_path: _Optional[_Iterable[bool]] = ..., current_monitoring_case_no_table_1: _Optional[int] = ..., current_monitoring_case_no_table_2: _Optional[int] = ..., current_monitoring_case_no_table_3: _Optional[int] = ..., current_monitoring_case_no_table_4: _Optional[int] = ..., application_error: bool = ..., device_error: bool = ...) -> None: ...
