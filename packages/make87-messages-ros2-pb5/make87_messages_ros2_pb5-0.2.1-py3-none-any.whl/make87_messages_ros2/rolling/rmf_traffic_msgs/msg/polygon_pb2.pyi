from make87_messages_ros2.rolling.rmf_traffic_msgs.msg import polygon_vertex_pb2 as _polygon_vertex_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Polygon(_message.Message):
    __slots__ = ("vertices",)
    VERTICES_FIELD_NUMBER: _ClassVar[int]
    vertices: _containers.RepeatedCompositeFieldContainer[_polygon_vertex_pb2.PolygonVertex]
    def __init__(self, vertices: _Optional[_Iterable[_Union[_polygon_vertex_pb2.PolygonVertex, _Mapping]]] = ...) -> None: ...
