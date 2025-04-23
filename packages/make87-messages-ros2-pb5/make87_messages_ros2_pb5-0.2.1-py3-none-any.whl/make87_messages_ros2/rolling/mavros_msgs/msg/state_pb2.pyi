from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class State(_message.Message):
    __slots__ = ("header", "connected", "armed", "guided", "manual_input", "mode", "system_status")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CONNECTED_FIELD_NUMBER: _ClassVar[int]
    ARMED_FIELD_NUMBER: _ClassVar[int]
    GUIDED_FIELD_NUMBER: _ClassVar[int]
    MANUAL_INPUT_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_STATUS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    connected: bool
    armed: bool
    guided: bool
    manual_input: bool
    mode: str
    system_status: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., connected: bool = ..., armed: bool = ..., guided: bool = ..., manual_input: bool = ..., mode: _Optional[str] = ..., system_status: _Optional[int] = ...) -> None: ...
