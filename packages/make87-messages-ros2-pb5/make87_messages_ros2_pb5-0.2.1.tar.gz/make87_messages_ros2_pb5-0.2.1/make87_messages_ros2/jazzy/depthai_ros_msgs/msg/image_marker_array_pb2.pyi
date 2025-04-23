from make87_messages_ros2.jazzy.visualization_msgs.msg import image_marker_pb2 as _image_marker_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ImageMarkerArray(_message.Message):
    __slots__ = ("markers",)
    MARKERS_FIELD_NUMBER: _ClassVar[int]
    markers: _containers.RepeatedCompositeFieldContainer[_image_marker_pb2.ImageMarker]
    def __init__(self, markers: _Optional[_Iterable[_Union[_image_marker_pb2.ImageMarker, _Mapping]]] = ...) -> None: ...
