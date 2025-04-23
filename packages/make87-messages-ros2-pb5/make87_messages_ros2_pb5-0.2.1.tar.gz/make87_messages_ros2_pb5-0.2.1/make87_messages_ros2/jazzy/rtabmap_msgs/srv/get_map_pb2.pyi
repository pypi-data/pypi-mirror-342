from make87_messages_ros2.jazzy.rtabmap_msgs.msg import map_data_pb2 as _map_data_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetMapRequest(_message.Message):
    __slots__ = ("global_map", "optimized", "graph_only")
    GLOBAL_MAP_FIELD_NUMBER: _ClassVar[int]
    OPTIMIZED_FIELD_NUMBER: _ClassVar[int]
    GRAPH_ONLY_FIELD_NUMBER: _ClassVar[int]
    global_map: bool
    optimized: bool
    graph_only: bool
    def __init__(self, global_map: bool = ..., optimized: bool = ..., graph_only: bool = ...) -> None: ...

class GetMapResponse(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _map_data_pb2.MapData
    def __init__(self, data: _Optional[_Union[_map_data_pb2.MapData, _Mapping]] = ...) -> None: ...
