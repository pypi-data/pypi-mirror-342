from make87_messages_ros2.rolling.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Session(_message.Message):
    __slots__ = ("request_time", "requester_id")
    REQUEST_TIME_FIELD_NUMBER: _ClassVar[int]
    REQUESTER_ID_FIELD_NUMBER: _ClassVar[int]
    request_time: _time_pb2.Time
    requester_id: str
    def __init__(self, request_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., requester_id: _Optional[str] = ...) -> None: ...
