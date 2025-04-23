from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ApplicationInputs(_message.Message):
    __slots__ = ("header", "unsafe_inputs_input_sources", "unsafe_inputs_flags", "monitoring_case_number_inputs", "monitoring_case_number_inputs_flags", "linear_velocity_inputs_velocity_0", "linear_velocity_inputs_velocity_0_valid", "linear_velocity_inputs_velocity_0_transmitted_safely", "linear_velocity_inputs_velocity_1", "linear_velocity_inputs_velocity_1_valid", "linear_velocity_inputs_velocity_1_transmitted_safely", "sleep_mode_input")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    UNSAFE_INPUTS_INPUT_SOURCES_FIELD_NUMBER: _ClassVar[int]
    UNSAFE_INPUTS_FLAGS_FIELD_NUMBER: _ClassVar[int]
    MONITORING_CASE_NUMBER_INPUTS_FIELD_NUMBER: _ClassVar[int]
    MONITORING_CASE_NUMBER_INPUTS_FLAGS_FIELD_NUMBER: _ClassVar[int]
    LINEAR_VELOCITY_INPUTS_VELOCITY_0_FIELD_NUMBER: _ClassVar[int]
    LINEAR_VELOCITY_INPUTS_VELOCITY_0_VALID_FIELD_NUMBER: _ClassVar[int]
    LINEAR_VELOCITY_INPUTS_VELOCITY_0_TRANSMITTED_SAFELY_FIELD_NUMBER: _ClassVar[int]
    LINEAR_VELOCITY_INPUTS_VELOCITY_1_FIELD_NUMBER: _ClassVar[int]
    LINEAR_VELOCITY_INPUTS_VELOCITY_1_VALID_FIELD_NUMBER: _ClassVar[int]
    LINEAR_VELOCITY_INPUTS_VELOCITY_1_TRANSMITTED_SAFELY_FIELD_NUMBER: _ClassVar[int]
    SLEEP_MODE_INPUT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    unsafe_inputs_input_sources: _containers.RepeatedScalarFieldContainer[bool]
    unsafe_inputs_flags: _containers.RepeatedScalarFieldContainer[bool]
    monitoring_case_number_inputs: _containers.RepeatedScalarFieldContainer[int]
    monitoring_case_number_inputs_flags: _containers.RepeatedScalarFieldContainer[bool]
    linear_velocity_inputs_velocity_0: int
    linear_velocity_inputs_velocity_0_valid: bool
    linear_velocity_inputs_velocity_0_transmitted_safely: bool
    linear_velocity_inputs_velocity_1: int
    linear_velocity_inputs_velocity_1_valid: bool
    linear_velocity_inputs_velocity_1_transmitted_safely: bool
    sleep_mode_input: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., unsafe_inputs_input_sources: _Optional[_Iterable[bool]] = ..., unsafe_inputs_flags: _Optional[_Iterable[bool]] = ..., monitoring_case_number_inputs: _Optional[_Iterable[int]] = ..., monitoring_case_number_inputs_flags: _Optional[_Iterable[bool]] = ..., linear_velocity_inputs_velocity_0: _Optional[int] = ..., linear_velocity_inputs_velocity_0_valid: bool = ..., linear_velocity_inputs_velocity_0_transmitted_safely: bool = ..., linear_velocity_inputs_velocity_1: _Optional[int] = ..., linear_velocity_inputs_velocity_1_valid: bool = ..., linear_velocity_inputs_velocity_1_transmitted_safely: bool = ..., sleep_mode_input: _Optional[int] = ...) -> None: ...
