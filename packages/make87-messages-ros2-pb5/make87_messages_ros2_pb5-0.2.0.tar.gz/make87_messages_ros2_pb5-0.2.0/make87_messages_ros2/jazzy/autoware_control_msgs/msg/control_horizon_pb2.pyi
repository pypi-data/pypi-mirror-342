from make87_messages_ros2.jazzy.autoware_control_msgs.msg import control_pb2 as _control_pb2
from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ControlHorizon(_message.Message):
    __slots__ = ("stamp", "control_time", "time_step_ms", "controls")
    STAMP_FIELD_NUMBER: _ClassVar[int]
    CONTROL_TIME_FIELD_NUMBER: _ClassVar[int]
    TIME_STEP_MS_FIELD_NUMBER: _ClassVar[int]
    CONTROLS_FIELD_NUMBER: _ClassVar[int]
    stamp: _time_pb2.Time
    control_time: _time_pb2.Time
    time_step_ms: float
    controls: _containers.RepeatedCompositeFieldContainer[_control_pb2.Control]
    def __init__(self, stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., control_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., time_step_ms: _Optional[float] = ..., controls: _Optional[_Iterable[_Union[_control_pb2.Control, _Mapping]]] = ...) -> None: ...
