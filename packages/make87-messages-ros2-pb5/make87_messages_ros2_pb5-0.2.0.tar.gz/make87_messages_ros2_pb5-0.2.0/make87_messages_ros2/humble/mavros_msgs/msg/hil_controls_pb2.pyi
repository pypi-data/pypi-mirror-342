from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HilControls(_message.Message):
    __slots__ = ("header", "ros2_header", "roll_ailerons", "pitch_elevator", "yaw_rudder", "throttle", "aux1", "aux2", "aux3", "aux4", "mode", "nav_mode")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    ROLL_AILERONS_FIELD_NUMBER: _ClassVar[int]
    PITCH_ELEVATOR_FIELD_NUMBER: _ClassVar[int]
    YAW_RUDDER_FIELD_NUMBER: _ClassVar[int]
    THROTTLE_FIELD_NUMBER: _ClassVar[int]
    AUX1_FIELD_NUMBER: _ClassVar[int]
    AUX2_FIELD_NUMBER: _ClassVar[int]
    AUX3_FIELD_NUMBER: _ClassVar[int]
    AUX4_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    NAV_MODE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    roll_ailerons: float
    pitch_elevator: float
    yaw_rudder: float
    throttle: float
    aux1: float
    aux2: float
    aux3: float
    aux4: float
    mode: int
    nav_mode: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., roll_ailerons: _Optional[float] = ..., pitch_elevator: _Optional[float] = ..., yaw_rudder: _Optional[float] = ..., throttle: _Optional[float] = ..., aux1: _Optional[float] = ..., aux2: _Optional[float] = ..., aux3: _Optional[float] = ..., aux4: _Optional[float] = ..., mode: _Optional[int] = ..., nav_mode: _Optional[int] = ...) -> None: ...
