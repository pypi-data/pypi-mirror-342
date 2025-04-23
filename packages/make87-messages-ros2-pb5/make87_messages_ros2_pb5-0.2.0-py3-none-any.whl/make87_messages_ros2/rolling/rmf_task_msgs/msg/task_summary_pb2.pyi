from make87_messages_ros2.rolling.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.rolling.rmf_task_msgs.msg import task_profile_pb2 as _task_profile_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TaskSummary(_message.Message):
    __slots__ = ("fleet_name", "task_id", "task_profile", "state", "status", "submission_time", "start_time", "end_time", "robot_name")
    FLEET_NAME_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    TASK_PROFILE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SUBMISSION_TIME_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    ROBOT_NAME_FIELD_NUMBER: _ClassVar[int]
    fleet_name: str
    task_id: str
    task_profile: _task_profile_pb2.TaskProfile
    state: int
    status: str
    submission_time: _time_pb2.Time
    start_time: _time_pb2.Time
    end_time: _time_pb2.Time
    robot_name: str
    def __init__(self, fleet_name: _Optional[str] = ..., task_id: _Optional[str] = ..., task_profile: _Optional[_Union[_task_profile_pb2.TaskProfile, _Mapping]] = ..., state: _Optional[int] = ..., status: _Optional[str] = ..., submission_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., start_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., end_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., robot_name: _Optional[str] = ...) -> None: ...
