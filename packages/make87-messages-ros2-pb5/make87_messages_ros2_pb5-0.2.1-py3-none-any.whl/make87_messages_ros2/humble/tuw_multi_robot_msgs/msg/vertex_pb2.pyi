from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import point_pb2 as _point_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Vertex(_message.Message):
    __slots__ = ("header", "id", "valid", "path", "weight", "width", "successors", "predecessors")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    VALID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    SUCCESSORS_FIELD_NUMBER: _ClassVar[int]
    PREDECESSORS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    id: int
    valid: bool
    path: _containers.RepeatedCompositeFieldContainer[_point_pb2.Point]
    weight: int
    width: float
    successors: _containers.RepeatedScalarFieldContainer[int]
    predecessors: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., id: _Optional[int] = ..., valid: bool = ..., path: _Optional[_Iterable[_Union[_point_pb2.Point, _Mapping]]] = ..., weight: _Optional[int] = ..., width: _Optional[float] = ..., successors: _Optional[_Iterable[int]] = ..., predecessors: _Optional[_Iterable[int]] = ...) -> None: ...
