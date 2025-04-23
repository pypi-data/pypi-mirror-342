from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IwsCmdVRATVec(_message.Message):
    __slots__ = ("header", "v", "rho", "phi", "delta_t", "state0")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    V_FIELD_NUMBER: _ClassVar[int]
    RHO_FIELD_NUMBER: _ClassVar[int]
    PHI_FIELD_NUMBER: _ClassVar[int]
    DELTA_T_FIELD_NUMBER: _ClassVar[int]
    STATE0_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    v: _containers.RepeatedScalarFieldContainer[float]
    rho: _containers.RepeatedScalarFieldContainer[float]
    phi: _containers.RepeatedScalarFieldContainer[float]
    delta_t: _containers.RepeatedScalarFieldContainer[float]
    state0: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., v: _Optional[_Iterable[float]] = ..., rho: _Optional[_Iterable[float]] = ..., phi: _Optional[_Iterable[float]] = ..., delta_t: _Optional[_Iterable[float]] = ..., state0: _Optional[_Iterable[float]] = ...) -> None: ...
