from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.jazzy.ibeo_msgs.msg import ibeo_data_header_pb2 as _ibeo_data_header_pb2
from make87_messages_ros2.jazzy.ibeo_msgs.msg import mounting_position_f_pb2 as _mounting_position_f_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CameraImage(_message.Message):
    __slots__ = ("header", "ibeo_header", "image_format", "us_since_power_on", "timestamp", "device_id", "mounting_position", "horizontal_opening_angle", "vertical_opening_angle", "image_width", "image_height", "compressed_size", "image_buffer")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    IBEO_HEADER_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FORMAT_FIELD_NUMBER: _ClassVar[int]
    US_SINCE_POWER_ON_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    MOUNTING_POSITION_FIELD_NUMBER: _ClassVar[int]
    HORIZONTAL_OPENING_ANGLE_FIELD_NUMBER: _ClassVar[int]
    VERTICAL_OPENING_ANGLE_FIELD_NUMBER: _ClassVar[int]
    IMAGE_WIDTH_FIELD_NUMBER: _ClassVar[int]
    IMAGE_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    COMPRESSED_SIZE_FIELD_NUMBER: _ClassVar[int]
    IMAGE_BUFFER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ibeo_header: _ibeo_data_header_pb2.IbeoDataHeader
    image_format: int
    us_since_power_on: int
    timestamp: _time_pb2.Time
    device_id: int
    mounting_position: _mounting_position_f_pb2.MountingPositionF
    horizontal_opening_angle: float
    vertical_opening_angle: float
    image_width: int
    image_height: int
    compressed_size: int
    image_buffer: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ibeo_header: _Optional[_Union[_ibeo_data_header_pb2.IbeoDataHeader, _Mapping]] = ..., image_format: _Optional[int] = ..., us_since_power_on: _Optional[int] = ..., timestamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., device_id: _Optional[int] = ..., mounting_position: _Optional[_Union[_mounting_position_f_pb2.MountingPositionF, _Mapping]] = ..., horizontal_opening_angle: _Optional[float] = ..., vertical_opening_angle: _Optional[float] = ..., image_width: _Optional[int] = ..., image_height: _Optional[int] = ..., compressed_size: _Optional[int] = ..., image_buffer: _Optional[_Iterable[int]] = ...) -> None: ...
