from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_pb2 as _pose_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetHandEyeCalibrationPoseRequest(_message.Message):
    __slots__ = ("slot", "pose")
    SLOT_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    slot: int
    pose: _pose_pb2.Pose
    def __init__(self, slot: _Optional[int] = ..., pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ...) -> None: ...

class SetHandEyeCalibrationPoseResponse(_message.Message):
    __slots__ = ("success", "status", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    status: int
    message: str
    def __init__(self, success: bool = ..., status: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...
