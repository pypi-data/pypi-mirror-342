from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.nav_msgs.msg import occupancy_grid_pb2 as _occupancy_grid_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LoadMapRequest(_message.Message):
    __slots__ = ("header", "map_url")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MAP_URL_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    map_url: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., map_url: _Optional[str] = ...) -> None: ...

class LoadMapResponse(_message.Message):
    __slots__ = ("header", "map", "result")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MAP_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    map: _occupancy_grid_pb2.OccupancyGrid
    result: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., map: _Optional[_Union[_occupancy_grid_pb2.OccupancyGrid, _Mapping]] = ..., result: _Optional[int] = ...) -> None: ...
