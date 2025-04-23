from make87_messages_ros2.rolling.polygon_msgs.msg import complex_polygon2_d_pb2 as _complex_polygon2_d_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ComplexPolygon2DStamped(_message.Message):
    __slots__ = ("header", "polygon")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    POLYGON_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    polygon: _complex_polygon2_d_pb2.ComplexPolygon2D
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., polygon: _Optional[_Union[_complex_polygon2_d_pb2.ComplexPolygon2D, _Mapping]] = ...) -> None: ...
