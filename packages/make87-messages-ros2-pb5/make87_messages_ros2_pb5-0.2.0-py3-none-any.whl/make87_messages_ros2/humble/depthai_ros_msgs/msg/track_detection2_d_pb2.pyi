from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.vision_msgs.msg import bounding_box2_d_pb2 as _bounding_box2_d_pb2
from make87_messages_ros2.humble.vision_msgs.msg import object_hypothesis_with_pose_pb2 as _object_hypothesis_with_pose_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TrackDetection2D(_message.Message):
    __slots__ = ("header", "results", "bbox", "is_tracking", "tracking_id", "tracking_age", "tracking_status")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    BBOX_FIELD_NUMBER: _ClassVar[int]
    IS_TRACKING_FIELD_NUMBER: _ClassVar[int]
    TRACKING_ID_FIELD_NUMBER: _ClassVar[int]
    TRACKING_AGE_FIELD_NUMBER: _ClassVar[int]
    TRACKING_STATUS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    results: _containers.RepeatedCompositeFieldContainer[_object_hypothesis_with_pose_pb2.ObjectHypothesisWithPose]
    bbox: _bounding_box2_d_pb2.BoundingBox2D
    is_tracking: bool
    tracking_id: str
    tracking_age: int
    tracking_status: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., results: _Optional[_Iterable[_Union[_object_hypothesis_with_pose_pb2.ObjectHypothesisWithPose, _Mapping]]] = ..., bbox: _Optional[_Union[_bounding_box2_d_pb2.BoundingBox2D, _Mapping]] = ..., is_tracking: bool = ..., tracking_id: _Optional[str] = ..., tracking_age: _Optional[int] = ..., tracking_status: _Optional[int] = ...) -> None: ...
