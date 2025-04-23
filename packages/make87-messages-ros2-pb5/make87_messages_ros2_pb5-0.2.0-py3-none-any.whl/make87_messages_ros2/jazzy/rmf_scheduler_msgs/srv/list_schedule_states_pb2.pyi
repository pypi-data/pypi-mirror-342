from make87_messages_ros2.jazzy.rmf_scheduler_msgs.msg import schedule_state_pb2 as _schedule_state_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListScheduleStatesRequest(_message.Message):
    __slots__ = ("modified_after",)
    MODIFIED_AFTER_FIELD_NUMBER: _ClassVar[int]
    modified_after: int
    def __init__(self, modified_after: _Optional[int] = ...) -> None: ...

class ListScheduleStatesResponse(_message.Message):
    __slots__ = ("success", "message", "schedules")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SCHEDULES_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    schedules: _containers.RepeatedCompositeFieldContainer[_schedule_state_pb2.ScheduleState]
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., schedules: _Optional[_Iterable[_Union[_schedule_state_pb2.ScheduleState, _Mapping]]] = ...) -> None: ...
