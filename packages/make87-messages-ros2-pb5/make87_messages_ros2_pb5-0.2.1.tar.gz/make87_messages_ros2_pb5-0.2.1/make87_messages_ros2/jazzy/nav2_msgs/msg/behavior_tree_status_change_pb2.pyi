from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BehaviorTreeStatusChange(_message.Message):
    __slots__ = ("timestamp", "node_name", "uid", "previous_status", "current_status")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_STATUS_FIELD_NUMBER: _ClassVar[int]
    CURRENT_STATUS_FIELD_NUMBER: _ClassVar[int]
    timestamp: _time_pb2.Time
    node_name: str
    uid: int
    previous_status: str
    current_status: str
    def __init__(self, timestamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., node_name: _Optional[str] = ..., uid: _Optional[int] = ..., previous_status: _Optional[str] = ..., current_status: _Optional[str] = ...) -> None: ...
