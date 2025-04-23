from make87_messages_ros2.rolling.moveit_msgs.msg import planner_params_pb2 as _planner_params_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetPlannerParamsRequest(_message.Message):
    __slots__ = ("pipeline_id", "planner_config", "group")
    PIPELINE_ID_FIELD_NUMBER: _ClassVar[int]
    PLANNER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    pipeline_id: str
    planner_config: str
    group: str
    def __init__(self, pipeline_id: _Optional[str] = ..., planner_config: _Optional[str] = ..., group: _Optional[str] = ...) -> None: ...

class GetPlannerParamsResponse(_message.Message):
    __slots__ = ("params",)
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: _planner_params_pb2.PlannerParams
    def __init__(self, params: _Optional[_Union[_planner_params_pb2.PlannerParams, _Mapping]] = ...) -> None: ...
