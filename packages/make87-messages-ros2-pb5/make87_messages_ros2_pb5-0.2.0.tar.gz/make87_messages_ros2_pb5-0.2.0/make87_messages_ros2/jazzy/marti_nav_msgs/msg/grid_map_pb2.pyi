from make87_messages_ros2.jazzy.geometry_msgs.msg import point_pb2 as _point_pb2
from make87_messages_ros2.jazzy.sensor_msgs.msg import image_pb2 as _image_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GridMap(_message.Message):
    __slots__ = ("header", "top_left", "top_right", "bottom_right", "bottom_left", "map_names", "map_data")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TOP_LEFT_FIELD_NUMBER: _ClassVar[int]
    TOP_RIGHT_FIELD_NUMBER: _ClassVar[int]
    BOTTOM_RIGHT_FIELD_NUMBER: _ClassVar[int]
    BOTTOM_LEFT_FIELD_NUMBER: _ClassVar[int]
    MAP_NAMES_FIELD_NUMBER: _ClassVar[int]
    MAP_DATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    top_left: _point_pb2.Point
    top_right: _point_pb2.Point
    bottom_right: _point_pb2.Point
    bottom_left: _point_pb2.Point
    map_names: _containers.RepeatedScalarFieldContainer[str]
    map_data: _containers.RepeatedCompositeFieldContainer[_image_pb2.Image]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., top_left: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., top_right: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., bottom_right: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., bottom_left: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., map_names: _Optional[_Iterable[str]] = ..., map_data: _Optional[_Iterable[_Union[_image_pb2.Image, _Mapping]]] = ...) -> None: ...
