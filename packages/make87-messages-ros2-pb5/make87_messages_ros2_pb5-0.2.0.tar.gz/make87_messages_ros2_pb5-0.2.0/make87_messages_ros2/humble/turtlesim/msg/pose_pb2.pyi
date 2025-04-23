from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Pose(_message.Message):
    __slots__ = ("header", "x", "y", "theta", "linear_velocity", "angular_velocity")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    THETA_FIELD_NUMBER: _ClassVar[int]
    LINEAR_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    x: float
    y: float
    theta: float
    linear_velocity: float
    angular_velocity: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., x: _Optional[float] = ..., y: _Optional[float] = ..., theta: _Optional[float] = ..., linear_velocity: _Optional[float] = ..., angular_velocity: _Optional[float] = ...) -> None: ...
