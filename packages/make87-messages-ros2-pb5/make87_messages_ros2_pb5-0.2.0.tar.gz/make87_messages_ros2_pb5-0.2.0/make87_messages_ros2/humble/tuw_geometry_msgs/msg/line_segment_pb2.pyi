from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import point_pb2 as _point_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LineSegment(_message.Message):
    __slots__ = ("header", "id", "p0", "p1")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    P0_FIELD_NUMBER: _ClassVar[int]
    P1_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    id: int
    p0: _point_pb2.Point
    p1: _point_pb2.Point
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., id: _Optional[int] = ..., p0: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., p1: _Optional[_Union[_point_pb2.Point, _Mapping]] = ...) -> None: ...
