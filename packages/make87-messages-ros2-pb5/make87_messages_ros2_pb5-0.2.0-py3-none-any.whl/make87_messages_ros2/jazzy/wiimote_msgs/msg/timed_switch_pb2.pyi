from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class TimedSwitch(_message.Message):
    __slots__ = ("switch_mode", "num_cycles", "pulse_pattern")
    SWITCH_MODE_FIELD_NUMBER: _ClassVar[int]
    NUM_CYCLES_FIELD_NUMBER: _ClassVar[int]
    PULSE_PATTERN_FIELD_NUMBER: _ClassVar[int]
    switch_mode: int
    num_cycles: int
    pulse_pattern: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, switch_mode: _Optional[int] = ..., num_cycles: _Optional[int] = ..., pulse_pattern: _Optional[_Iterable[float]] = ...) -> None: ...
