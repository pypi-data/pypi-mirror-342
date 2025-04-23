from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PedestrianImageID(_message.Message):
    __slots__ = ("header", "ros2_header", "pixel_x", "pixel_y", "image_width", "image_height")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    PIXEL_X_FIELD_NUMBER: _ClassVar[int]
    PIXEL_Y_FIELD_NUMBER: _ClassVar[int]
    IMAGE_WIDTH_FIELD_NUMBER: _ClassVar[int]
    IMAGE_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    pixel_x: int
    pixel_y: int
    image_width: int
    image_height: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., pixel_x: _Optional[int] = ..., pixel_y: _Optional[int] = ..., image_width: _Optional[int] = ..., image_height: _Optional[int] = ...) -> None: ...
