from make87_messages_ros2.rolling.geometry_msgs.msg import pose_pb2 as _pose_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SubmapTexture(_message.Message):
    __slots__ = ("cells", "width", "height", "resolution", "slice_pose")
    CELLS_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    SLICE_POSE_FIELD_NUMBER: _ClassVar[int]
    cells: _containers.RepeatedScalarFieldContainer[int]
    width: int
    height: int
    resolution: float
    slice_pose: _pose_pb2.Pose
    def __init__(self, cells: _Optional[_Iterable[int]] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., resolution: _Optional[float] = ..., slice_pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ...) -> None: ...
