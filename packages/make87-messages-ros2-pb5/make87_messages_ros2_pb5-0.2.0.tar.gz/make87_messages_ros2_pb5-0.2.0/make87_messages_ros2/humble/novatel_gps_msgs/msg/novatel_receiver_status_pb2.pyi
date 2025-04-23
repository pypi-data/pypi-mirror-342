from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NovatelReceiverStatus(_message.Message):
    __slots__ = ("header", "original_status_code", "error_flag", "temperature_flag", "voltage_supply_flag", "antenna_powered", "antenna_is_open", "antenna_is_shorted", "cpu_overload_flag", "com1_buffer_overrun", "com2_buffer_overrun", "com3_buffer_overrun", "usb_buffer_overrun", "rf1_agc_flag", "rf2_agc_flag", "almanac_flag", "position_solution_flag", "position_fixed_flag", "clock_steering_status_enabled", "clock_model_flag", "oemv_external_oscillator_flag", "software_resource_flag", "aux1_status_event_flag", "aux2_status_event_flag", "aux3_status_event_flag")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FLAG_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FLAG_FIELD_NUMBER: _ClassVar[int]
    VOLTAGE_SUPPLY_FLAG_FIELD_NUMBER: _ClassVar[int]
    ANTENNA_POWERED_FIELD_NUMBER: _ClassVar[int]
    ANTENNA_IS_OPEN_FIELD_NUMBER: _ClassVar[int]
    ANTENNA_IS_SHORTED_FIELD_NUMBER: _ClassVar[int]
    CPU_OVERLOAD_FLAG_FIELD_NUMBER: _ClassVar[int]
    COM1_BUFFER_OVERRUN_FIELD_NUMBER: _ClassVar[int]
    COM2_BUFFER_OVERRUN_FIELD_NUMBER: _ClassVar[int]
    COM3_BUFFER_OVERRUN_FIELD_NUMBER: _ClassVar[int]
    USB_BUFFER_OVERRUN_FIELD_NUMBER: _ClassVar[int]
    RF1_AGC_FLAG_FIELD_NUMBER: _ClassVar[int]
    RF2_AGC_FLAG_FIELD_NUMBER: _ClassVar[int]
    ALMANAC_FLAG_FIELD_NUMBER: _ClassVar[int]
    POSITION_SOLUTION_FLAG_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIXED_FLAG_FIELD_NUMBER: _ClassVar[int]
    CLOCK_STEERING_STATUS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    CLOCK_MODEL_FLAG_FIELD_NUMBER: _ClassVar[int]
    OEMV_EXTERNAL_OSCILLATOR_FLAG_FIELD_NUMBER: _ClassVar[int]
    SOFTWARE_RESOURCE_FLAG_FIELD_NUMBER: _ClassVar[int]
    AUX1_STATUS_EVENT_FLAG_FIELD_NUMBER: _ClassVar[int]
    AUX2_STATUS_EVENT_FLAG_FIELD_NUMBER: _ClassVar[int]
    AUX3_STATUS_EVENT_FLAG_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    original_status_code: int
    error_flag: bool
    temperature_flag: bool
    voltage_supply_flag: bool
    antenna_powered: bool
    antenna_is_open: bool
    antenna_is_shorted: bool
    cpu_overload_flag: bool
    com1_buffer_overrun: bool
    com2_buffer_overrun: bool
    com3_buffer_overrun: bool
    usb_buffer_overrun: bool
    rf1_agc_flag: bool
    rf2_agc_flag: bool
    almanac_flag: bool
    position_solution_flag: bool
    position_fixed_flag: bool
    clock_steering_status_enabled: bool
    clock_model_flag: bool
    oemv_external_oscillator_flag: bool
    software_resource_flag: bool
    aux1_status_event_flag: bool
    aux2_status_event_flag: bool
    aux3_status_event_flag: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., original_status_code: _Optional[int] = ..., error_flag: bool = ..., temperature_flag: bool = ..., voltage_supply_flag: bool = ..., antenna_powered: bool = ..., antenna_is_open: bool = ..., antenna_is_shorted: bool = ..., cpu_overload_flag: bool = ..., com1_buffer_overrun: bool = ..., com2_buffer_overrun: bool = ..., com3_buffer_overrun: bool = ..., usb_buffer_overrun: bool = ..., rf1_agc_flag: bool = ..., rf2_agc_flag: bool = ..., almanac_flag: bool = ..., position_solution_flag: bool = ..., position_fixed_flag: bool = ..., clock_steering_status_enabled: bool = ..., clock_model_flag: bool = ..., oemv_external_oscillator_flag: bool = ..., software_resource_flag: bool = ..., aux1_status_event_flag: bool = ..., aux2_status_event_flag: bool = ..., aux3_status_event_flag: bool = ...) -> None: ...
