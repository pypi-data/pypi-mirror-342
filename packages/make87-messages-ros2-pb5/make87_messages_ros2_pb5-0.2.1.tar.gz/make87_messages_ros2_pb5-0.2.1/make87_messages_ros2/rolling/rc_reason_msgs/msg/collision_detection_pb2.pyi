from make87_messages_ros2.rolling.geometry_msgs.msg import point_pb2 as _point_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CollisionDetection(_message.Message):
    __slots__ = ("gripper_id", "pre_grasp_offset")
    GRIPPER_ID_FIELD_NUMBER: _ClassVar[int]
    PRE_GRASP_OFFSET_FIELD_NUMBER: _ClassVar[int]
    gripper_id: str
    pre_grasp_offset: _point_pb2.Point
    def __init__(self, gripper_id: _Optional[str] = ..., pre_grasp_offset: _Optional[_Union[_point_pb2.Point, _Mapping]] = ...) -> None: ...
