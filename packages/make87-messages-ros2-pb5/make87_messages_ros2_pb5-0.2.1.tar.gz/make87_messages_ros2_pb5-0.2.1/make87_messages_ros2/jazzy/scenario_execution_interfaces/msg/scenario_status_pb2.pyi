from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScenarioStatus(_message.Message):
    __slots__ = ("system_time", "ros_time", "data")
    SYSTEM_TIME_FIELD_NUMBER: _ClassVar[int]
    ROS_TIME_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    system_time: _time_pb2.Time
    ros_time: _time_pb2.Time
    data: str
    def __init__(self, system_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., ros_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., data: _Optional[str] = ...) -> None: ...
