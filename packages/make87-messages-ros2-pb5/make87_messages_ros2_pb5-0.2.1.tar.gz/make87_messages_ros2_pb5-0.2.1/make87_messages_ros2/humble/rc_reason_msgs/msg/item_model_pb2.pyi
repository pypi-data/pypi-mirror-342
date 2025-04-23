from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rc_reason_msgs.msg import range_box_pb2 as _range_box_pb2
from make87_messages_ros2.humble.rc_reason_msgs.msg import range_rectangle_pb2 as _range_rectangle_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ItemModel(_message.Message):
    __slots__ = ("header", "type", "unknown", "rectangle")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN_FIELD_NUMBER: _ClassVar[int]
    RECTANGLE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    type: str
    unknown: _range_box_pb2.RangeBox
    rectangle: _range_rectangle_pb2.RangeRectangle
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., type: _Optional[str] = ..., unknown: _Optional[_Union[_range_box_pb2.RangeBox, _Mapping]] = ..., rectangle: _Optional[_Union[_range_rectangle_pb2.RangeRectangle, _Mapping]] = ...) -> None: ...
