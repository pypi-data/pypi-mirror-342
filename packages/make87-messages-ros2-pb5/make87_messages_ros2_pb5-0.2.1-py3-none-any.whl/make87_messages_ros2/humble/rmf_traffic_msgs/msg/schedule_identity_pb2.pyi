from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScheduleIdentity(_message.Message):
    __slots__ = ("header", "node_uuid", "timestamp")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NODE_UUID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    node_uuid: str
    timestamp: _time_pb2.Time
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., node_uuid: _Optional[str] = ..., timestamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ...) -> None: ...
