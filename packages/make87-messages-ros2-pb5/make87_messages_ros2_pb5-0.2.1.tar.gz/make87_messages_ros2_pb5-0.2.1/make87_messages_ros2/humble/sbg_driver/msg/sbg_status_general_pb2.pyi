from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SbgStatusGeneral(_message.Message):
    __slots__ = ("header", "main_power", "imu_power", "gps_power", "settings", "temperature", "datalogger", "cpu")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MAIN_POWER_FIELD_NUMBER: _ClassVar[int]
    IMU_POWER_FIELD_NUMBER: _ClassVar[int]
    GPS_POWER_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    DATALOGGER_FIELD_NUMBER: _ClassVar[int]
    CPU_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    main_power: bool
    imu_power: bool
    gps_power: bool
    settings: bool
    temperature: bool
    datalogger: bool
    cpu: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., main_power: bool = ..., imu_power: bool = ..., gps_power: bool = ..., settings: bool = ..., temperature: bool = ..., datalogger: bool = ..., cpu: bool = ...) -> None: ...
