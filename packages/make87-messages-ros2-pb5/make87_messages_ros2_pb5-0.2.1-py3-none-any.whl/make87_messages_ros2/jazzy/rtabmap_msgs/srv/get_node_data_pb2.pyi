from make87_messages_ros2.jazzy.rtabmap_msgs.msg import node_pb2 as _node_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetNodeDataRequest(_message.Message):
    __slots__ = ("ids", "images", "scan", "grid", "user_data")
    IDS_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    SCAN_FIELD_NUMBER: _ClassVar[int]
    GRID_FIELD_NUMBER: _ClassVar[int]
    USER_DATA_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[int]
    images: bool
    scan: bool
    grid: bool
    user_data: bool
    def __init__(self, ids: _Optional[_Iterable[int]] = ..., images: bool = ..., scan: bool = ..., grid: bool = ..., user_data: bool = ...) -> None: ...

class GetNodeDataResponse(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[_node_pb2.Node]
    def __init__(self, data: _Optional[_Iterable[_Union[_node_pb2.Node, _Mapping]]] = ...) -> None: ...
