from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import point_pb2 as _point_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose2_d_pb2 as _pose2_d_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HandLandmark(_message.Message):
    __slots__ = ("header", "label", "lm_score", "landmark", "position", "is_spatial")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    LM_SCORE_FIELD_NUMBER: _ClassVar[int]
    LANDMARK_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    IS_SPATIAL_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    label: str
    lm_score: float
    landmark: _containers.RepeatedCompositeFieldContainer[_pose2_d_pb2.Pose2D]
    position: _point_pb2.Point
    is_spatial: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., label: _Optional[str] = ..., lm_score: _Optional[float] = ..., landmark: _Optional[_Iterable[_Union[_pose2_d_pb2.Pose2D, _Mapping]]] = ..., position: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., is_spatial: bool = ...) -> None: ...
