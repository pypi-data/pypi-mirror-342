from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import polygon_stamped_pb2 as _polygon_stamped_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PolygonList(_message.Message):
    __slots__ = ("header", "polygons")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    POLYGONS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    polygons: _containers.RepeatedCompositeFieldContainer[_polygon_stamped_pb2.PolygonStamped]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., polygons: _Optional[_Iterable[_Union[_polygon_stamped_pb2.PolygonStamped, _Mapping]]] = ...) -> None: ...
