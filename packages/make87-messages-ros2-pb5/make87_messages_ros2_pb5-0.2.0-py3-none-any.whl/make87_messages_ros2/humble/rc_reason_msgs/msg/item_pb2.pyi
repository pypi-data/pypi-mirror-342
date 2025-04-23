from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_stamped_pb2 as _pose_stamped_pb2
from make87_messages_ros2.humble.rc_reason_msgs.msg import rectangle_pb2 as _rectangle_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Item(_message.Message):
    __slots__ = ("header", "uuid", "grasp_uuids", "type", "rectangle", "pose")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    GRASP_UUIDS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    RECTANGLE_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    uuid: str
    grasp_uuids: _containers.RepeatedScalarFieldContainer[str]
    type: str
    rectangle: _rectangle_pb2.Rectangle
    pose: _pose_stamped_pb2.PoseStamped
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., uuid: _Optional[str] = ..., grasp_uuids: _Optional[_Iterable[str]] = ..., type: _Optional[str] = ..., rectangle: _Optional[_Union[_rectangle_pb2.Rectangle, _Mapping]] = ..., pose: _Optional[_Union[_pose_stamped_pb2.PoseStamped, _Mapping]] = ...) -> None: ...
