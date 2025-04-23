from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.jazzy.pendulum_msgs.msg import joint_command_pb2 as _joint_command_pb2
from make87_messages_ros2.jazzy.pendulum_msgs.msg import joint_state_pb2 as _joint_state_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RttestResults(_message.Message):
    __slots__ = ("stamp", "command", "state", "cur_latency", "mean_latency", "min_latency", "max_latency", "minor_pagefaults", "major_pagefaults")
    STAMP_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    CUR_LATENCY_FIELD_NUMBER: _ClassVar[int]
    MEAN_LATENCY_FIELD_NUMBER: _ClassVar[int]
    MIN_LATENCY_FIELD_NUMBER: _ClassVar[int]
    MAX_LATENCY_FIELD_NUMBER: _ClassVar[int]
    MINOR_PAGEFAULTS_FIELD_NUMBER: _ClassVar[int]
    MAJOR_PAGEFAULTS_FIELD_NUMBER: _ClassVar[int]
    stamp: _time_pb2.Time
    command: _joint_command_pb2.JointCommand
    state: _joint_state_pb2.JointState
    cur_latency: int
    mean_latency: float
    min_latency: int
    max_latency: int
    minor_pagefaults: int
    major_pagefaults: int
    def __init__(self, stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., command: _Optional[_Union[_joint_command_pb2.JointCommand, _Mapping]] = ..., state: _Optional[_Union[_joint_state_pb2.JointState, _Mapping]] = ..., cur_latency: _Optional[int] = ..., mean_latency: _Optional[float] = ..., min_latency: _Optional[int] = ..., max_latency: _Optional[int] = ..., minor_pagefaults: _Optional[int] = ..., major_pagefaults: _Optional[int] = ...) -> None: ...
