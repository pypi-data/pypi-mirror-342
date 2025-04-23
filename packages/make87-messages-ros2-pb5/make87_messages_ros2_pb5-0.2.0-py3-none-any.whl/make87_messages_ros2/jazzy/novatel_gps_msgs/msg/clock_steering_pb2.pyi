from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ClockSteering(_message.Message):
    __slots__ = ("source", "steering_state", "period", "pulse_width", "bandwidth", "slope", "offset", "drift_rate")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    STEERING_STATE_FIELD_NUMBER: _ClassVar[int]
    PERIOD_FIELD_NUMBER: _ClassVar[int]
    PULSE_WIDTH_FIELD_NUMBER: _ClassVar[int]
    BANDWIDTH_FIELD_NUMBER: _ClassVar[int]
    SLOPE_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    DRIFT_RATE_FIELD_NUMBER: _ClassVar[int]
    source: str
    steering_state: str
    period: int
    pulse_width: float
    bandwidth: float
    slope: float
    offset: float
    drift_rate: float
    def __init__(self, source: _Optional[str] = ..., steering_state: _Optional[str] = ..., period: _Optional[int] = ..., pulse_width: _Optional[float] = ..., bandwidth: _Optional[float] = ..., slope: _Optional[float] = ..., offset: _Optional[float] = ..., drift_rate: _Optional[float] = ...) -> None: ...
