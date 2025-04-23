from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import duration_pb2 as _duration_pb2
from make87_messages_ros2.humble.rmf_obstacle_msgs.msg import bounding_box3_d_pb2 as _bounding_box3_d_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Obstacle(_message.Message):
    __slots__ = ("header", "ros2_header", "id", "source", "level_name", "classification", "bbox", "data_resolution", "data", "lifetime", "action")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    LEVEL_NAME_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_FIELD_NUMBER: _ClassVar[int]
    BBOX_FIELD_NUMBER: _ClassVar[int]
    DATA_RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    LIFETIME_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    id: int
    source: str
    level_name: str
    classification: str
    bbox: _bounding_box3_d_pb2.BoundingBox3D
    data_resolution: float
    data: _containers.RepeatedScalarFieldContainer[int]
    lifetime: _duration_pb2.Duration
    action: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., id: _Optional[int] = ..., source: _Optional[str] = ..., level_name: _Optional[str] = ..., classification: _Optional[str] = ..., bbox: _Optional[_Union[_bounding_box3_d_pb2.BoundingBox3D, _Mapping]] = ..., data_resolution: _Optional[float] = ..., data: _Optional[_Iterable[int]] = ..., lifetime: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., action: _Optional[int] = ...) -> None: ...
