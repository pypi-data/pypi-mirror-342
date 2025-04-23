from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import point_pb2 as _point_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Fiducial(_message.Message):
    __slots__ = ("header", "ids", "ids_confidence", "object_points", "image_points")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    IDS_FIELD_NUMBER: _ClassVar[int]
    IDS_CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_POINTS_FIELD_NUMBER: _ClassVar[int]
    IMAGE_POINTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ids: _containers.RepeatedScalarFieldContainer[int]
    ids_confidence: _containers.RepeatedScalarFieldContainer[float]
    object_points: _containers.RepeatedCompositeFieldContainer[_point_pb2.Point]
    image_points: _containers.RepeatedCompositeFieldContainer[_point_pb2.Point]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ids: _Optional[_Iterable[int]] = ..., ids_confidence: _Optional[_Iterable[float]] = ..., object_points: _Optional[_Iterable[_Union[_point_pb2.Point, _Mapping]]] = ..., image_points: _Optional[_Iterable[_Union[_point_pb2.Point, _Mapping]]] = ...) -> None: ...
