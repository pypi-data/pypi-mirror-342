from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PriorityConfigCmd(_message.Message):
    __slots__ = ("header", "confirm", "handshake_priority", "auto_reply_priority", "scheduled_priority", "polled_priority")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CONFIRM_FIELD_NUMBER: _ClassVar[int]
    HANDSHAKE_PRIORITY_FIELD_NUMBER: _ClassVar[int]
    AUTO_REPLY_PRIORITY_FIELD_NUMBER: _ClassVar[int]
    SCHEDULED_PRIORITY_FIELD_NUMBER: _ClassVar[int]
    POLLED_PRIORITY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    confirm: bool
    handshake_priority: int
    auto_reply_priority: int
    scheduled_priority: int
    polled_priority: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., confirm: bool = ..., handshake_priority: _Optional[int] = ..., auto_reply_priority: _Optional[int] = ..., scheduled_priority: _Optional[int] = ..., polled_priority: _Optional[int] = ...) -> None: ...
