from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.fadecandy_msgs.msg import led_strip_pb2 as _led_strip_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LEDArray(_message.Message):
    __slots__ = ("header", "strips")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STRIPS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    strips: _containers.RepeatedCompositeFieldContainer[_led_strip_pb2.LEDStrip]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., strips: _Optional[_Iterable[_Union[_led_strip_pb2.LEDStrip, _Mapping]]] = ...) -> None: ...
