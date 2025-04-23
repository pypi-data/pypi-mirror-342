from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import image_pb2 as _image_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import region_of_interest_pb2 as _region_of_interest_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DisparityImage(_message.Message):
    __slots__ = ("header", "ros2_header", "image", "f", "t", "valid_window", "min_disparity", "max_disparity", "delta_d")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    F_FIELD_NUMBER: _ClassVar[int]
    T_FIELD_NUMBER: _ClassVar[int]
    VALID_WINDOW_FIELD_NUMBER: _ClassVar[int]
    MIN_DISPARITY_FIELD_NUMBER: _ClassVar[int]
    MAX_DISPARITY_FIELD_NUMBER: _ClassVar[int]
    DELTA_D_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    image: _image_pb2.Image
    f: float
    t: float
    valid_window: _region_of_interest_pb2.RegionOfInterest
    min_disparity: float
    max_disparity: float
    delta_d: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., image: _Optional[_Union[_image_pb2.Image, _Mapping]] = ..., f: _Optional[float] = ..., t: _Optional[float] = ..., valid_window: _Optional[_Union[_region_of_interest_pb2.RegionOfInterest, _Mapping]] = ..., min_disparity: _Optional[float] = ..., max_disparity: _Optional[float] = ..., delta_d: _Optional[float] = ...) -> None: ...
