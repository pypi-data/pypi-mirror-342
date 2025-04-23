from make87_messages_ros2.rolling.irobot_create_msgs.msg import led_color_pb2 as _led_color_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LightringLeds(_message.Message):
    __slots__ = ("header", "leds", "override_system")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LEDS_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    leds: _containers.RepeatedCompositeFieldContainer[_led_color_pb2.LedColor]
    override_system: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., leds: _Optional[_Iterable[_Union[_led_color_pb2.LedColor, _Mapping]]] = ..., override_system: bool = ...) -> None: ...
