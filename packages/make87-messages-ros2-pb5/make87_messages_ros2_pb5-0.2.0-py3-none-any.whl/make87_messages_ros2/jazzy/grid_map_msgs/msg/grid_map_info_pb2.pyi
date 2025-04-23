from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_pb2 as _pose_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GridMapInfo(_message.Message):
    __slots__ = ("resolution", "length_x", "length_y", "pose")
    RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    LENGTH_X_FIELD_NUMBER: _ClassVar[int]
    LENGTH_Y_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    resolution: float
    length_x: float
    length_y: float
    pose: _pose_pb2.Pose
    def __init__(self, resolution: _Optional[float] = ..., length_x: _Optional[float] = ..., length_y: _Optional[float] = ..., pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ...) -> None: ...
