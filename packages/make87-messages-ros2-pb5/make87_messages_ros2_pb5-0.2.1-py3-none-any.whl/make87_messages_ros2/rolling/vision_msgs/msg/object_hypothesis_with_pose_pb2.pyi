from make87_messages_ros2.rolling.geometry_msgs.msg import pose_with_covariance_pb2 as _pose_with_covariance_pb2
from make87_messages_ros2.rolling.vision_msgs.msg import object_hypothesis_pb2 as _object_hypothesis_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ObjectHypothesisWithPose(_message.Message):
    __slots__ = ("hypothesis", "pose")
    HYPOTHESIS_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    hypothesis: _object_hypothesis_pb2.ObjectHypothesis
    pose: _pose_with_covariance_pb2.PoseWithCovariance
    def __init__(self, hypothesis: _Optional[_Union[_object_hypothesis_pb2.ObjectHypothesis, _Mapping]] = ..., pose: _Optional[_Union[_pose_with_covariance_pb2.PoseWithCovariance, _Mapping]] = ...) -> None: ...
