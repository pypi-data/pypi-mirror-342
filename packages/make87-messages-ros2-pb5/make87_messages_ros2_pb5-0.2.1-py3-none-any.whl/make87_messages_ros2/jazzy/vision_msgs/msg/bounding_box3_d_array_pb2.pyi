from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.jazzy.vision_msgs.msg import bounding_box3_d_pb2 as _bounding_box3_d_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BoundingBox3DArray(_message.Message):
    __slots__ = ("header", "boxes")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BOXES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    boxes: _containers.RepeatedCompositeFieldContainer[_bounding_box3_d_pb2.BoundingBox3D]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., boxes: _Optional[_Iterable[_Union[_bounding_box3_d_pb2.BoundingBox3D, _Mapping]]] = ...) -> None: ...
