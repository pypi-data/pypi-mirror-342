from make87_messages_ros2.jazzy.visualization_msgs.msg import marker_pb2 as _marker_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MarkerArray(_message.Message):
    __slots__ = ("markers",)
    MARKERS_FIELD_NUMBER: _ClassVar[int]
    markers: _containers.RepeatedCompositeFieldContainer[_marker_pb2.Marker]
    def __init__(self, markers: _Optional[_Iterable[_Union[_marker_pb2.Marker, _Mapping]]] = ...) -> None: ...
