from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DiffDriveCmdVWVec(_message.Message):
    __slots__ = ("header", "ros2_header", "v", "w", "delta_t", "state0")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    V_FIELD_NUMBER: _ClassVar[int]
    W_FIELD_NUMBER: _ClassVar[int]
    DELTA_T_FIELD_NUMBER: _ClassVar[int]
    STATE0_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    v: _containers.RepeatedScalarFieldContainer[float]
    w: _containers.RepeatedScalarFieldContainer[float]
    delta_t: _containers.RepeatedScalarFieldContainer[float]
    state0: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., v: _Optional[_Iterable[float]] = ..., w: _Optional[_Iterable[float]] = ..., delta_t: _Optional[_Iterable[float]] = ..., state0: _Optional[_Iterable[float]] = ...) -> None: ...
