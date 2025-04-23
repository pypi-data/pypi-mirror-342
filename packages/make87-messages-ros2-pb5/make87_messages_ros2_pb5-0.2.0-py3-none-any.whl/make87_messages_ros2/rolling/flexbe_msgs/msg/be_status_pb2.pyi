from make87_messages_ros2.rolling.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BEStatus(_message.Message):
    __slots__ = ("stamp", "behavior_id", "code", "args")
    STAMP_FIELD_NUMBER: _ClassVar[int]
    BEHAVIOR_ID_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    stamp: _time_pb2.Time
    behavior_id: int
    code: int
    args: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., behavior_id: _Optional[int] = ..., code: _Optional[int] = ..., args: _Optional[_Iterable[str]] = ...) -> None: ...
