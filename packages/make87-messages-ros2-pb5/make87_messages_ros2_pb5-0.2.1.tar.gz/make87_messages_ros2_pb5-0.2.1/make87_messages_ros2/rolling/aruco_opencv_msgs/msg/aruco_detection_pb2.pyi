from make87_messages_ros2.rolling.aruco_opencv_msgs.msg import board_pose_pb2 as _board_pose_pb2
from make87_messages_ros2.rolling.aruco_opencv_msgs.msg import marker_pose_pb2 as _marker_pose_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ArucoDetection(_message.Message):
    __slots__ = ("header", "markers", "boards")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MARKERS_FIELD_NUMBER: _ClassVar[int]
    BOARDS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    markers: _containers.RepeatedCompositeFieldContainer[_marker_pose_pb2.MarkerPose]
    boards: _containers.RepeatedCompositeFieldContainer[_board_pose_pb2.BoardPose]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., markers: _Optional[_Iterable[_Union[_marker_pose_pb2.MarkerPose, _Mapping]]] = ..., boards: _Optional[_Iterable[_Union[_board_pose_pb2.BoardPose, _Mapping]]] = ...) -> None: ...
