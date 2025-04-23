from make87_messages_ros2.jazzy.geometry_msgs.msg import twist_pb2 as _twist_pb2
from make87_messages_ros2.jazzy.lgsvl_msgs.msg import bounding_box2_d_pb2 as _bounding_box2_d_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Detection2D(_message.Message):
    __slots__ = ("header", "id", "label", "score", "bbox", "velocity")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    BBOX_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    id: int
    label: str
    score: float
    bbox: _bounding_box2_d_pb2.BoundingBox2D
    velocity: _twist_pb2.Twist
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., id: _Optional[int] = ..., label: _Optional[str] = ..., score: _Optional[float] = ..., bbox: _Optional[_Union[_bounding_box2_d_pb2.BoundingBox2D, _Mapping]] = ..., velocity: _Optional[_Union[_twist_pb2.Twist, _Mapping]] = ...) -> None: ...
