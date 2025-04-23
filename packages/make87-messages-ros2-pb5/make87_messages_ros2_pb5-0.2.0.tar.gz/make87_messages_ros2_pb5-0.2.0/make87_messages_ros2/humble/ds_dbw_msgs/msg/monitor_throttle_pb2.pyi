from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.ds_dbw_msgs.msg import quality_pb2 as _quality_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MonitorThrottle(_message.Message):
    __slots__ = ("header", "ros2_header", "pedal_pc", "pedal_qf")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    PEDAL_PC_FIELD_NUMBER: _ClassVar[int]
    PEDAL_QF_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    pedal_pc: float
    pedal_qf: _quality_pb2.Quality
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., pedal_pc: _Optional[float] = ..., pedal_qf: _Optional[_Union[_quality_pb2.Quality, _Mapping]] = ...) -> None: ...
