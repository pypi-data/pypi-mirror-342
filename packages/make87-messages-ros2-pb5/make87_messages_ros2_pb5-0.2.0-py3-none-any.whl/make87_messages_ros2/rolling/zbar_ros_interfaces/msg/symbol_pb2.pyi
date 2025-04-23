from make87_messages_ros2.rolling.vision_msgs.msg import point2_d_pb2 as _point2_d_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Symbol(_message.Message):
    __slots__ = ("data", "points")
    DATA_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    data: str
    points: _containers.RepeatedCompositeFieldContainer[_point2_d_pb2.Point2D]
    def __init__(self, data: _Optional[str] = ..., points: _Optional[_Iterable[_Union[_point2_d_pb2.Point2D, _Mapping]]] = ...) -> None: ...
