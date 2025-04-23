from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ApplicationOutputs(_message.Message):
    __slots__ = ("header", "evaluation_path_outputs_eval_out", "evaluation_path_outputs_is_safe", "evaluation_path_outputs_is_valid", "monitoring_case_number_outputs", "monitoring_case_number_outputs_flags", "sleep_mode_output", "sleep_mode_output_valid", "error_flag_contamination_warning", "error_flag_contamination_error", "error_flag_manipulation_error", "error_flag_glare", "error_flag_reference_contour_intruded", "error_flag_critical_error", "error_flags_are_valid", "linear_velocity_outputs_velocity_0", "linear_velocity_outputs_velocity_0_valid", "linear_velocity_outputs_velocity_0_transmitted_safely", "linear_velocity_outputs_velocity_1", "linear_velocity_outputs_velocity_1_valid", "linear_velocity_outputs_velocity_1_transmitted_safely", "resulting_velocity", "resulting_velocity_flags")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    EVALUATION_PATH_OUTPUTS_EVAL_OUT_FIELD_NUMBER: _ClassVar[int]
    EVALUATION_PATH_OUTPUTS_IS_SAFE_FIELD_NUMBER: _ClassVar[int]
    EVALUATION_PATH_OUTPUTS_IS_VALID_FIELD_NUMBER: _ClassVar[int]
    MONITORING_CASE_NUMBER_OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    MONITORING_CASE_NUMBER_OUTPUTS_FLAGS_FIELD_NUMBER: _ClassVar[int]
    SLEEP_MODE_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    SLEEP_MODE_OUTPUT_VALID_FIELD_NUMBER: _ClassVar[int]
    ERROR_FLAG_CONTAMINATION_WARNING_FIELD_NUMBER: _ClassVar[int]
    ERROR_FLAG_CONTAMINATION_ERROR_FIELD_NUMBER: _ClassVar[int]
    ERROR_FLAG_MANIPULATION_ERROR_FIELD_NUMBER: _ClassVar[int]
    ERROR_FLAG_GLARE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FLAG_REFERENCE_CONTOUR_INTRUDED_FIELD_NUMBER: _ClassVar[int]
    ERROR_FLAG_CRITICAL_ERROR_FIELD_NUMBER: _ClassVar[int]
    ERROR_FLAGS_ARE_VALID_FIELD_NUMBER: _ClassVar[int]
    LINEAR_VELOCITY_OUTPUTS_VELOCITY_0_FIELD_NUMBER: _ClassVar[int]
    LINEAR_VELOCITY_OUTPUTS_VELOCITY_0_VALID_FIELD_NUMBER: _ClassVar[int]
    LINEAR_VELOCITY_OUTPUTS_VELOCITY_0_TRANSMITTED_SAFELY_FIELD_NUMBER: _ClassVar[int]
    LINEAR_VELOCITY_OUTPUTS_VELOCITY_1_FIELD_NUMBER: _ClassVar[int]
    LINEAR_VELOCITY_OUTPUTS_VELOCITY_1_VALID_FIELD_NUMBER: _ClassVar[int]
    LINEAR_VELOCITY_OUTPUTS_VELOCITY_1_TRANSMITTED_SAFELY_FIELD_NUMBER: _ClassVar[int]
    RESULTING_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    RESULTING_VELOCITY_FLAGS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    evaluation_path_outputs_eval_out: _containers.RepeatedScalarFieldContainer[bool]
    evaluation_path_outputs_is_safe: _containers.RepeatedScalarFieldContainer[bool]
    evaluation_path_outputs_is_valid: _containers.RepeatedScalarFieldContainer[bool]
    monitoring_case_number_outputs: _containers.RepeatedScalarFieldContainer[int]
    monitoring_case_number_outputs_flags: _containers.RepeatedScalarFieldContainer[bool]
    sleep_mode_output: int
    sleep_mode_output_valid: bool
    error_flag_contamination_warning: bool
    error_flag_contamination_error: bool
    error_flag_manipulation_error: bool
    error_flag_glare: bool
    error_flag_reference_contour_intruded: bool
    error_flag_critical_error: bool
    error_flags_are_valid: bool
    linear_velocity_outputs_velocity_0: int
    linear_velocity_outputs_velocity_0_valid: bool
    linear_velocity_outputs_velocity_0_transmitted_safely: bool
    linear_velocity_outputs_velocity_1: int
    linear_velocity_outputs_velocity_1_valid: bool
    linear_velocity_outputs_velocity_1_transmitted_safely: bool
    resulting_velocity: _containers.RepeatedScalarFieldContainer[int]
    resulting_velocity_flags: _containers.RepeatedScalarFieldContainer[bool]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., evaluation_path_outputs_eval_out: _Optional[_Iterable[bool]] = ..., evaluation_path_outputs_is_safe: _Optional[_Iterable[bool]] = ..., evaluation_path_outputs_is_valid: _Optional[_Iterable[bool]] = ..., monitoring_case_number_outputs: _Optional[_Iterable[int]] = ..., monitoring_case_number_outputs_flags: _Optional[_Iterable[bool]] = ..., sleep_mode_output: _Optional[int] = ..., sleep_mode_output_valid: bool = ..., error_flag_contamination_warning: bool = ..., error_flag_contamination_error: bool = ..., error_flag_manipulation_error: bool = ..., error_flag_glare: bool = ..., error_flag_reference_contour_intruded: bool = ..., error_flag_critical_error: bool = ..., error_flags_are_valid: bool = ..., linear_velocity_outputs_velocity_0: _Optional[int] = ..., linear_velocity_outputs_velocity_0_valid: bool = ..., linear_velocity_outputs_velocity_0_transmitted_safely: bool = ..., linear_velocity_outputs_velocity_1: _Optional[int] = ..., linear_velocity_outputs_velocity_1_valid: bool = ..., linear_velocity_outputs_velocity_1_transmitted_safely: bool = ..., resulting_velocity: _Optional[_Iterable[int]] = ..., resulting_velocity_flags: _Optional[_Iterable[bool]] = ...) -> None: ...
