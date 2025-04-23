from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_with_covariance_pb2 as _pose_with_covariance_pb2
from make87_messages_ros2.humble.vision_msgs.msg import object_hypothesis_pb2 as _object_hypothesis_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ObjectHypothesisWithPose(_message.Message):
    __slots__ = ("header", "hypothesis", "pose")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    HYPOTHESIS_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    hypothesis: _object_hypothesis_pb2.ObjectHypothesis
    pose: _pose_with_covariance_pb2.PoseWithCovariance
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., hypothesis: _Optional[_Union[_object_hypothesis_pb2.ObjectHypothesis, _Mapping]] = ..., pose: _Optional[_Union[_pose_with_covariance_pb2.PoseWithCovariance, _Mapping]] = ...) -> None: ...
