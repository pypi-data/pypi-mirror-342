from make87_messages_ros2.jazzy.moveit_msgs.msg import planning_scene_pb2 as _planning_scene_pb2
from make87_messages_ros2.jazzy.moveit_msgs.msg import planning_scene_components_pb2 as _planning_scene_components_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetPlanningSceneRequest(_message.Message):
    __slots__ = ("components",)
    COMPONENTS_FIELD_NUMBER: _ClassVar[int]
    components: _planning_scene_components_pb2.PlanningSceneComponents
    def __init__(self, components: _Optional[_Union[_planning_scene_components_pb2.PlanningSceneComponents, _Mapping]] = ...) -> None: ...

class GetPlanningSceneResponse(_message.Message):
    __slots__ = ("scene",)
    SCENE_FIELD_NUMBER: _ClassVar[int]
    scene: _planning_scene_pb2.PlanningScene
    def __init__(self, scene: _Optional[_Union[_planning_scene_pb2.PlanningScene, _Mapping]] = ...) -> None: ...
