from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Pose(_message.Message):
    __slots__ = ("x", "y", "theta", "linear_velocity", "angular_velocity")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    THETA_FIELD_NUMBER: _ClassVar[int]
    LINEAR_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    theta: float
    linear_velocity: float
    angular_velocity: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ..., theta: _Optional[float] = ..., linear_velocity: _Optional[float] = ..., angular_velocity: _Optional[float] = ...) -> None: ...
