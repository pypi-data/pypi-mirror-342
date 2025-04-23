from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IwsCmdVRAT(_message.Message):
    __slots__ = ("header", "ros2_header", "v", "rho", "phi", "delta_t")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    V_FIELD_NUMBER: _ClassVar[int]
    RHO_FIELD_NUMBER: _ClassVar[int]
    PHI_FIELD_NUMBER: _ClassVar[int]
    DELTA_T_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    v: float
    rho: float
    phi: float
    delta_t: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., v: _Optional[float] = ..., rho: _Optional[float] = ..., phi: _Optional[float] = ..., delta_t: _Optional[float] = ...) -> None: ...
