from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_stamped_pb2 as _pose_stamped_pb2
from make87_messages_ros2.jazzy.nav_msgs.msg import path_pb2 as _path_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetPlanRequest(_message.Message):
    __slots__ = ("start", "goal", "tolerance")
    START_FIELD_NUMBER: _ClassVar[int]
    GOAL_FIELD_NUMBER: _ClassVar[int]
    TOLERANCE_FIELD_NUMBER: _ClassVar[int]
    start: _pose_stamped_pb2.PoseStamped
    goal: _pose_stamped_pb2.PoseStamped
    tolerance: float
    def __init__(self, start: _Optional[_Union[_pose_stamped_pb2.PoseStamped, _Mapping]] = ..., goal: _Optional[_Union[_pose_stamped_pb2.PoseStamped, _Mapping]] = ..., tolerance: _Optional[float] = ...) -> None: ...

class GetPlanResponse(_message.Message):
    __slots__ = ("plan",)
    PLAN_FIELD_NUMBER: _ClassVar[int]
    plan: _path_pb2.Path
    def __init__(self, plan: _Optional[_Union[_path_pb2.Path, _Mapping]] = ...) -> None: ...
