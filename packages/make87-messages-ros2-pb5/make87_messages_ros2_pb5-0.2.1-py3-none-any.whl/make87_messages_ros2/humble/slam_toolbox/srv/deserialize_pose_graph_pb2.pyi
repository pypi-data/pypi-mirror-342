from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose2_d_pb2 as _pose2_d_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DeserializePoseGraphRequest(_message.Message):
    __slots__ = ("header", "filename", "match_type", "initial_pose")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    MATCH_TYPE_FIELD_NUMBER: _ClassVar[int]
    INITIAL_POSE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    filename: str
    match_type: int
    initial_pose: _pose2_d_pb2.Pose2D
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., filename: _Optional[str] = ..., match_type: _Optional[int] = ..., initial_pose: _Optional[_Union[_pose2_d_pb2.Pose2D, _Mapping]] = ...) -> None: ...

class DeserializePoseGraphResponse(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...
