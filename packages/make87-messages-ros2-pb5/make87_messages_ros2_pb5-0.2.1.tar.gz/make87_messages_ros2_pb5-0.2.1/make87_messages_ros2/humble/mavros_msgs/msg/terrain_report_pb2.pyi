from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TerrainReport(_message.Message):
    __slots__ = ("header", "ros2_header", "latitude", "longitude", "spacing", "terrain_height", "current_height", "pending", "loaded")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    SPACING_FIELD_NUMBER: _ClassVar[int]
    TERRAIN_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    CURRENT_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    PENDING_FIELD_NUMBER: _ClassVar[int]
    LOADED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    latitude: float
    longitude: float
    spacing: int
    terrain_height: float
    current_height: float
    pending: int
    loaded: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., spacing: _Optional[int] = ..., terrain_height: _Optional[float] = ..., current_height: _Optional[float] = ..., pending: _Optional[int] = ..., loaded: _Optional[int] = ...) -> None: ...
