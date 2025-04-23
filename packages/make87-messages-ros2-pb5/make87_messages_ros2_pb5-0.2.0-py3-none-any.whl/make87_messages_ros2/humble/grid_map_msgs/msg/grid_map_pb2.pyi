from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.grid_map_msgs.msg import grid_map_info_pb2 as _grid_map_info_pb2
from make87_messages_ros2.humble.std_msgs.msg import float32_multi_array_pb2 as _float32_multi_array_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GridMap(_message.Message):
    __slots__ = ("header", "ros2_header", "info", "layers", "basic_layers", "data", "outer_start_index", "inner_start_index")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    BASIC_LAYERS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    OUTER_START_INDEX_FIELD_NUMBER: _ClassVar[int]
    INNER_START_INDEX_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    info: _grid_map_info_pb2.GridMapInfo
    layers: _containers.RepeatedScalarFieldContainer[str]
    basic_layers: _containers.RepeatedScalarFieldContainer[str]
    data: _containers.RepeatedCompositeFieldContainer[_float32_multi_array_pb2.Float32MultiArray]
    outer_start_index: int
    inner_start_index: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., info: _Optional[_Union[_grid_map_info_pb2.GridMapInfo, _Mapping]] = ..., layers: _Optional[_Iterable[str]] = ..., basic_layers: _Optional[_Iterable[str]] = ..., data: _Optional[_Iterable[_Union[_float32_multi_array_pb2.Float32MultiArray, _Mapping]]] = ..., outer_start_index: _Optional[int] = ..., inner_start_index: _Optional[int] = ...) -> None: ...
