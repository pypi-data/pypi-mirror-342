from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BaseConstr(_message.Message):
    __slots__ = ("header", "ros2_header", "v_max", "av_max", "w_max", "aw_max", "omg_wh_max")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    V_MAX_FIELD_NUMBER: _ClassVar[int]
    AV_MAX_FIELD_NUMBER: _ClassVar[int]
    W_MAX_FIELD_NUMBER: _ClassVar[int]
    AW_MAX_FIELD_NUMBER: _ClassVar[int]
    OMG_WH_MAX_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    v_max: float
    av_max: float
    w_max: float
    aw_max: float
    omg_wh_max: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., v_max: _Optional[float] = ..., av_max: _Optional[float] = ..., w_max: _Optional[float] = ..., aw_max: _Optional[float] = ..., omg_wh_max: _Optional[float] = ...) -> None: ...
