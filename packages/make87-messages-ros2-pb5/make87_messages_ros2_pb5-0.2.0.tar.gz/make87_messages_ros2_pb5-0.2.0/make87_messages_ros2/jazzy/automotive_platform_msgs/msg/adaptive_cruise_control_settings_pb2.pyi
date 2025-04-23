from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AdaptiveCruiseControlSettings(_message.Message):
    __slots__ = ("header", "set_speed", "following_spot", "min_percent", "step_percent", "cipv_percent", "max_distance")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SET_SPEED_FIELD_NUMBER: _ClassVar[int]
    FOLLOWING_SPOT_FIELD_NUMBER: _ClassVar[int]
    MIN_PERCENT_FIELD_NUMBER: _ClassVar[int]
    STEP_PERCENT_FIELD_NUMBER: _ClassVar[int]
    CIPV_PERCENT_FIELD_NUMBER: _ClassVar[int]
    MAX_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    set_speed: float
    following_spot: int
    min_percent: float
    step_percent: float
    cipv_percent: float
    max_distance: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., set_speed: _Optional[float] = ..., following_spot: _Optional[int] = ..., min_percent: _Optional[float] = ..., step_percent: _Optional[float] = ..., cipv_percent: _Optional[float] = ..., max_distance: _Optional[float] = ...) -> None: ...
