from make87_messages_ros2.jazzy.builtin_interfaces.msg import duration_pb2 as _duration_pb2
from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_pb2 as _pose_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PredictedPath(_message.Message):
    __slots__ = ("path", "time_step", "confidence")
    PATH_FIELD_NUMBER: _ClassVar[int]
    TIME_STEP_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    path: _containers.RepeatedCompositeFieldContainer[_pose_pb2.Pose]
    time_step: _duration_pb2.Duration
    confidence: float
    def __init__(self, path: _Optional[_Iterable[_Union[_pose_pb2.Pose, _Mapping]]] = ..., time_step: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., confidence: _Optional[float] = ...) -> None: ...
