from make87_messages_ros2.rolling.std_msgs.msg import color_rgba_pb2 as _color_rgba_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LeftFootLed(_message.Message):
    __slots__ = ("color",)
    COLOR_FIELD_NUMBER: _ClassVar[int]
    color: _color_rgba_pb2.ColorRGBA
    def __init__(self, color: _Optional[_Union[_color_rgba_pb2.ColorRGBA, _Mapping]] = ...) -> None: ...
