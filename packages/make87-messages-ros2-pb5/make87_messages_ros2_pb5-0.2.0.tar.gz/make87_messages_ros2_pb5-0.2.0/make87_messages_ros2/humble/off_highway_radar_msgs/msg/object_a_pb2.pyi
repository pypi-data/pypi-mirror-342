from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import point_pb2 as _point_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import twist_pb2 as _twist_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ObjectA(_message.Message):
    __slots__ = ("header", "can_id", "stamp", "id", "position", "velocity", "meas", "valid", "hist")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CAN_ID_FIELD_NUMBER: _ClassVar[int]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_FIELD_NUMBER: _ClassVar[int]
    MEAS_FIELD_NUMBER: _ClassVar[int]
    VALID_FIELD_NUMBER: _ClassVar[int]
    HIST_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    can_id: int
    stamp: _time_pb2.Time
    id: int
    position: _point_pb2.Point
    velocity: _twist_pb2.Twist
    meas: bool
    valid: bool
    hist: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., can_id: _Optional[int] = ..., stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., id: _Optional[int] = ..., position: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., velocity: _Optional[_Union[_twist_pb2.Twist, _Mapping]] = ..., meas: bool = ..., valid: bool = ..., hist: bool = ...) -> None: ...
