from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Loop(_message.Message):
    __slots__ = ("task_id", "robot_type", "num_loops", "start_name", "finish_name")
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    ROBOT_TYPE_FIELD_NUMBER: _ClassVar[int]
    NUM_LOOPS_FIELD_NUMBER: _ClassVar[int]
    START_NAME_FIELD_NUMBER: _ClassVar[int]
    FINISH_NAME_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    robot_type: str
    num_loops: int
    start_name: str
    finish_name: str
    def __init__(self, task_id: _Optional[str] = ..., robot_type: _Optional[str] = ..., num_loops: _Optional[int] = ..., start_name: _Optional[str] = ..., finish_name: _Optional[str] = ...) -> None: ...
