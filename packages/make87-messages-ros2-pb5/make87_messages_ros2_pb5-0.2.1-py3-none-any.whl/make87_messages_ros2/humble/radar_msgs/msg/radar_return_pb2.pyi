from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RadarReturn(_message.Message):
    __slots__ = ("header", "range", "azimuth", "elevation", "doppler_velocity", "amplitude")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RANGE_FIELD_NUMBER: _ClassVar[int]
    AZIMUTH_FIELD_NUMBER: _ClassVar[int]
    ELEVATION_FIELD_NUMBER: _ClassVar[int]
    DOPPLER_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    AMPLITUDE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    range: float
    azimuth: float
    elevation: float
    doppler_velocity: float
    amplitude: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., range: _Optional[float] = ..., azimuth: _Optional[float] = ..., elevation: _Optional[float] = ..., doppler_velocity: _Optional[float] = ..., amplitude: _Optional[float] = ...) -> None: ...
