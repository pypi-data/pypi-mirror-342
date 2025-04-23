from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.pcl_msgs.msg import vertices_pb2 as _vertices_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import point_cloud2_pb2 as _point_cloud2_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PolygonMesh(_message.Message):
    __slots__ = ("header", "ros2_header", "cloud", "polygons")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    CLOUD_FIELD_NUMBER: _ClassVar[int]
    POLYGONS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    cloud: _point_cloud2_pb2.PointCloud2
    polygons: _containers.RepeatedCompositeFieldContainer[_vertices_pb2.Vertices]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., cloud: _Optional[_Union[_point_cloud2_pb2.PointCloud2, _Mapping]] = ..., polygons: _Optional[_Iterable[_Union[_vertices_pb2.Vertices, _Mapping]]] = ...) -> None: ...
