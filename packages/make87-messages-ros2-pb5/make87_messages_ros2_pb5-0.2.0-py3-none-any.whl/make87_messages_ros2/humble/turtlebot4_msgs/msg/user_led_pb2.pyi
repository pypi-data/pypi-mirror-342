from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UserLed(_message.Message):
    __slots__ = ("header", "led", "color", "blink_period", "duty_cycle")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LED_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    BLINK_PERIOD_FIELD_NUMBER: _ClassVar[int]
    DUTY_CYCLE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    led: int
    color: int
    blink_period: int
    duty_cycle: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., led: _Optional[int] = ..., color: _Optional[int] = ..., blink_period: _Optional[int] = ..., duty_cycle: _Optional[float] = ...) -> None: ...
