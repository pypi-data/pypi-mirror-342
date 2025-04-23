from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AIMPlusStatus(_message.Message):
    __slots__ = ("header", "tow", "wnc", "interference", "spoofing", "osnma_authenticating", "galileo_authentic", "galileo_spoofed", "gps_authentic", "gps_spoofed")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TOW_FIELD_NUMBER: _ClassVar[int]
    WNC_FIELD_NUMBER: _ClassVar[int]
    INTERFERENCE_FIELD_NUMBER: _ClassVar[int]
    SPOOFING_FIELD_NUMBER: _ClassVar[int]
    OSNMA_AUTHENTICATING_FIELD_NUMBER: _ClassVar[int]
    GALILEO_AUTHENTIC_FIELD_NUMBER: _ClassVar[int]
    GALILEO_SPOOFED_FIELD_NUMBER: _ClassVar[int]
    GPS_AUTHENTIC_FIELD_NUMBER: _ClassVar[int]
    GPS_SPOOFED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    tow: int
    wnc: int
    interference: int
    spoofing: int
    osnma_authenticating: bool
    galileo_authentic: int
    galileo_spoofed: int
    gps_authentic: int
    gps_spoofed: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., tow: _Optional[int] = ..., wnc: _Optional[int] = ..., interference: _Optional[int] = ..., spoofing: _Optional[int] = ..., osnma_authenticating: bool = ..., galileo_authentic: _Optional[int] = ..., galileo_spoofed: _Optional[int] = ..., gps_authentic: _Optional[int] = ..., gps_spoofed: _Optional[int] = ...) -> None: ...
