from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ControlModeCommandRequest(_message.Message):
    __slots__ = ("stamp", "mode")
    STAMP_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    stamp: _time_pb2.Time
    mode: int
    def __init__(self, stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., mode: _Optional[int] = ...) -> None: ...

class ControlModeCommandResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
