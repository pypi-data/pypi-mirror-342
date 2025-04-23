from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Leds(_message.Message):
    __slots__ = ("led0", "led1", "led2", "led3")
    LED0_FIELD_NUMBER: _ClassVar[int]
    LED1_FIELD_NUMBER: _ClassVar[int]
    LED2_FIELD_NUMBER: _ClassVar[int]
    LED3_FIELD_NUMBER: _ClassVar[int]
    led0: bool
    led1: bool
    led2: bool
    led3: bool
    def __init__(self, led0: bool = ..., led1: bool = ..., led2: bool = ..., led3: bool = ...) -> None: ...
