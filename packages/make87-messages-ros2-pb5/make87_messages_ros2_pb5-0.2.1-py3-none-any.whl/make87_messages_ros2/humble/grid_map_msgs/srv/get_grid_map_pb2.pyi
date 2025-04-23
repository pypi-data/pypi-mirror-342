from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.grid_map_msgs.msg import grid_map_pb2 as _grid_map_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetGridMapRequest(_message.Message):
    __slots__ = ("header", "frame_id", "position_x", "position_y", "length_x", "length_y", "layers")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FRAME_ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_X_FIELD_NUMBER: _ClassVar[int]
    POSITION_Y_FIELD_NUMBER: _ClassVar[int]
    LENGTH_X_FIELD_NUMBER: _ClassVar[int]
    LENGTH_Y_FIELD_NUMBER: _ClassVar[int]
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    frame_id: str
    position_x: float
    position_y: float
    length_x: float
    length_y: float
    layers: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., frame_id: _Optional[str] = ..., position_x: _Optional[float] = ..., position_y: _Optional[float] = ..., length_x: _Optional[float] = ..., length_y: _Optional[float] = ..., layers: _Optional[_Iterable[str]] = ...) -> None: ...

class GetGridMapResponse(_message.Message):
    __slots__ = ("header", "map")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MAP_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    map: _grid_map_pb2.GridMap
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., map: _Optional[_Union[_grid_map_pb2.GridMap, _Mapping]] = ...) -> None: ...
