from make87_messages_ros2.jazzy.geometry_msgs.msg import point32_pb2 as _point32_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Polygon(_message.Message):
    __slots__ = ("points",)
    POINTS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedCompositeFieldContainer[_point32_pb2.Point32]
    def __init__(self, points: _Optional[_Iterable[_Union[_point32_pb2.Point32, _Mapping]]] = ...) -> None: ...
