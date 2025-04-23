from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import point_pb2 as _point_pb2
from make87_messages_ros2.humble.shape_msgs.msg import mesh_triangle_pb2 as _mesh_triangle_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Mesh(_message.Message):
    __slots__ = ("header", "triangles", "vertices")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TRIANGLES_FIELD_NUMBER: _ClassVar[int]
    VERTICES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    triangles: _containers.RepeatedCompositeFieldContainer[_mesh_triangle_pb2.MeshTriangle]
    vertices: _containers.RepeatedCompositeFieldContainer[_point_pb2.Point]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., triangles: _Optional[_Iterable[_Union[_mesh_triangle_pb2.MeshTriangle, _Mapping]]] = ..., vertices: _Optional[_Iterable[_Union[_point_pb2.Point, _Mapping]]] = ...) -> None: ...
