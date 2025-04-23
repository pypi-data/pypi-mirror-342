from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TransmissionFeedback(_message.Message):
    __slots__ = ("header", "current_range", "stable", "reverse", "forward")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CURRENT_RANGE_FIELD_NUMBER: _ClassVar[int]
    STABLE_FIELD_NUMBER: _ClassVar[int]
    REVERSE_FIELD_NUMBER: _ClassVar[int]
    FORWARD_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    current_range: str
    stable: bool
    reverse: bool
    forward: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., current_range: _Optional[str] = ..., stable: bool = ..., reverse: bool = ..., forward: bool = ...) -> None: ...
