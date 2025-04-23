from make87_messages_ros2.jazzy.std_msgs.msg import color_rgba_pb2 as _color_rgba_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OverlayText(_message.Message):
    __slots__ = ("action", "width", "height", "horizontal_distance", "vertical_distance", "horizontal_alignment", "vertical_alignment", "bg_color", "line_width", "text_size", "font", "fg_color", "text")
    ACTION_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    HORIZONTAL_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    VERTICAL_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    HORIZONTAL_ALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    VERTICAL_ALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    BG_COLOR_FIELD_NUMBER: _ClassVar[int]
    LINE_WIDTH_FIELD_NUMBER: _ClassVar[int]
    TEXT_SIZE_FIELD_NUMBER: _ClassVar[int]
    FONT_FIELD_NUMBER: _ClassVar[int]
    FG_COLOR_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    action: int
    width: int
    height: int
    horizontal_distance: int
    vertical_distance: int
    horizontal_alignment: int
    vertical_alignment: int
    bg_color: _color_rgba_pb2.ColorRGBA
    line_width: int
    text_size: float
    font: str
    fg_color: _color_rgba_pb2.ColorRGBA
    text: str
    def __init__(self, action: _Optional[int] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., horizontal_distance: _Optional[int] = ..., vertical_distance: _Optional[int] = ..., horizontal_alignment: _Optional[int] = ..., vertical_alignment: _Optional[int] = ..., bg_color: _Optional[_Union[_color_rgba_pb2.ColorRGBA, _Mapping]] = ..., line_width: _Optional[int] = ..., text_size: _Optional[float] = ..., font: _Optional[str] = ..., fg_color: _Optional[_Union[_color_rgba_pb2.ColorRGBA, _Mapping]] = ..., text: _Optional[str] = ...) -> None: ...
