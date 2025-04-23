from make87_messages_ros2.jazzy.geometry_msgs.msg import point_pb2 as _point_pb2
from make87_messages_ros2.jazzy.vision_msgs.msg import bounding_box2_d_pb2 as _bounding_box2_d_pb2
from make87_messages_ros2.jazzy.vision_msgs.msg import object_hypothesis_pb2 as _object_hypothesis_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SpatialDetection(_message.Message):
    __slots__ = ("results", "bbox", "position", "is_tracking", "tracking_id")
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    BBOX_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    IS_TRACKING_FIELD_NUMBER: _ClassVar[int]
    TRACKING_ID_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[_object_hypothesis_pb2.ObjectHypothesis]
    bbox: _bounding_box2_d_pb2.BoundingBox2D
    position: _point_pb2.Point
    is_tracking: bool
    tracking_id: str
    def __init__(self, results: _Optional[_Iterable[_Union[_object_hypothesis_pb2.ObjectHypothesis, _Mapping]]] = ..., bbox: _Optional[_Union[_bounding_box2_d_pb2.BoundingBox2D, _Mapping]] = ..., position: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., is_tracking: bool = ..., tracking_id: _Optional[str] = ...) -> None: ...
