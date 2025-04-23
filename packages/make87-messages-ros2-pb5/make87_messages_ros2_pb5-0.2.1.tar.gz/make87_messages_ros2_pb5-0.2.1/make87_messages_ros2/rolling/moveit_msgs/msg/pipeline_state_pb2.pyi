from make87_messages_ros2.rolling.moveit_msgs.msg import motion_plan_request_pb2 as _motion_plan_request_pb2
from make87_messages_ros2.rolling.moveit_msgs.msg import motion_plan_response_pb2 as _motion_plan_response_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PipelineState(_message.Message):
    __slots__ = ("request", "response", "pipeline_stage")
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_STAGE_FIELD_NUMBER: _ClassVar[int]
    request: _motion_plan_request_pb2.MotionPlanRequest
    response: _motion_plan_response_pb2.MotionPlanResponse
    pipeline_stage: str
    def __init__(self, request: _Optional[_Union[_motion_plan_request_pb2.MotionPlanRequest, _Mapping]] = ..., response: _Optional[_Union[_motion_plan_response_pb2.MotionPlanResponse, _Mapping]] = ..., pipeline_stage: _Optional[str] = ...) -> None: ...
