from make87_messages_ros2.jazzy.moveit_msgs.msg import planning_scene_pb2 as _planning_scene_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PlanningOptions(_message.Message):
    __slots__ = ("planning_scene_diff", "plan_only", "look_around", "look_around_attempts", "max_safe_execution_cost", "replan", "replan_attempts", "replan_delay")
    PLANNING_SCENE_DIFF_FIELD_NUMBER: _ClassVar[int]
    PLAN_ONLY_FIELD_NUMBER: _ClassVar[int]
    LOOK_AROUND_FIELD_NUMBER: _ClassVar[int]
    LOOK_AROUND_ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
    MAX_SAFE_EXECUTION_COST_FIELD_NUMBER: _ClassVar[int]
    REPLAN_FIELD_NUMBER: _ClassVar[int]
    REPLAN_ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
    REPLAN_DELAY_FIELD_NUMBER: _ClassVar[int]
    planning_scene_diff: _planning_scene_pb2.PlanningScene
    plan_only: bool
    look_around: bool
    look_around_attempts: int
    max_safe_execution_cost: float
    replan: bool
    replan_attempts: int
    replan_delay: float
    def __init__(self, planning_scene_diff: _Optional[_Union[_planning_scene_pb2.PlanningScene, _Mapping]] = ..., plan_only: bool = ..., look_around: bool = ..., look_around_attempts: _Optional[int] = ..., max_safe_execution_cost: _Optional[float] = ..., replan: bool = ..., replan_attempts: _Optional[int] = ..., replan_delay: _Optional[float] = ...) -> None: ...
