from make87_messages_ros2.rolling.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ServiceEventInfo(_message.Message):
    __slots__ = ("event_type", "stamp", "client_gid", "sequence_number")
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    CLIENT_GID_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    event_type: int
    stamp: _time_pb2.Time
    client_gid: _containers.RepeatedScalarFieldContainer[int]
    sequence_number: int
    def __init__(self, event_type: _Optional[int] = ..., stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., client_gid: _Optional[_Iterable[int]] = ..., sequence_number: _Optional[int] = ...) -> None: ...
