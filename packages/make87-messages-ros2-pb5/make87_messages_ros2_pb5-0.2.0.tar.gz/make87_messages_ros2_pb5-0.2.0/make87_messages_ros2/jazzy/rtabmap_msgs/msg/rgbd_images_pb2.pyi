from make87_messages_ros2.jazzy.rtabmap_msgs.msg import rgbd_image_pb2 as _rgbd_image_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RGBDImages(_message.Message):
    __slots__ = ("header", "rgbd_images")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RGBD_IMAGES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    rgbd_images: _containers.RepeatedCompositeFieldContainer[_rgbd_image_pb2.RGBDImage]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., rgbd_images: _Optional[_Iterable[_Union[_rgbd_image_pb2.RGBDImage, _Mapping]]] = ...) -> None: ...
