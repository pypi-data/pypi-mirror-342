from make87_messages_ros2.jazzy.rmf_task_msgs.msg import task_description_pb2 as _task_description_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SubmitTaskRequest(_message.Message):
    __slots__ = ("requester", "description")
    REQUESTER_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    requester: str
    description: _task_description_pb2.TaskDescription
    def __init__(self, requester: _Optional[str] = ..., description: _Optional[_Union[_task_description_pb2.TaskDescription, _Mapping]] = ...) -> None: ...

class SubmitTaskResponse(_message.Message):
    __slots__ = ("success", "task_id", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    task_id: str
    message: str
    def __init__(self, success: bool = ..., task_id: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...
