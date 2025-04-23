from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Status(_message.Message):
    __slots__ = ("header", "device_number", "device_name", "bus_voltage", "temperature", "output_voltage", "analog_input", "mode", "fault")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DEVICE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    BUS_VOLTAGE_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_VOLTAGE_FIELD_NUMBER: _ClassVar[int]
    ANALOG_INPUT_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    FAULT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    device_number: int
    device_name: str
    bus_voltage: float
    temperature: float
    output_voltage: float
    analog_input: float
    mode: int
    fault: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., device_number: _Optional[int] = ..., device_name: _Optional[str] = ..., bus_voltage: _Optional[float] = ..., temperature: _Optional[float] = ..., output_voltage: _Optional[float] = ..., analog_input: _Optional[float] = ..., mode: _Optional[int] = ..., fault: _Optional[int] = ...) -> None: ...
