from make87_messages_ros2.jazzy.cartographer_ros_msgs.msg import status_response_pb2 as _status_response_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FinishTrajectoryRequest(_message.Message):
    __slots__ = ("trajectory_id",)
    TRAJECTORY_ID_FIELD_NUMBER: _ClassVar[int]
    trajectory_id: int
    def __init__(self, trajectory_id: _Optional[int] = ...) -> None: ...

class FinishTrajectoryResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _status_response_pb2.StatusResponse
    def __init__(self, status: _Optional[_Union[_status_response_pb2.StatusResponse, _Mapping]] = ...) -> None: ...
