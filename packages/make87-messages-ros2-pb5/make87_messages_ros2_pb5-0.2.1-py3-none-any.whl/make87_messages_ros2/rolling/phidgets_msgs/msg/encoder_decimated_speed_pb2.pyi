from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EncoderDecimatedSpeed(_message.Message):
    __slots__ = ("header", "avr_speed")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    AVR_SPEED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    avr_speed: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., avr_speed: _Optional[float] = ...) -> None: ...
