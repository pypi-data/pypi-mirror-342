from make87_messages_ros2.jazzy.moveit_msgs.msg import object_color_pb2 as _object_color_pb2
from make87_messages_ros2.jazzy.moveit_msgs.msg import robot_state_pb2 as _robot_state_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DisplayRobotState(_message.Message):
    __slots__ = ("state", "highlight_links", "hide")
    STATE_FIELD_NUMBER: _ClassVar[int]
    HIGHLIGHT_LINKS_FIELD_NUMBER: _ClassVar[int]
    HIDE_FIELD_NUMBER: _ClassVar[int]
    state: _robot_state_pb2.RobotState
    highlight_links: _containers.RepeatedCompositeFieldContainer[_object_color_pb2.ObjectColor]
    hide: bool
    def __init__(self, state: _Optional[_Union[_robot_state_pb2.RobotState, _Mapping]] = ..., highlight_links: _Optional[_Iterable[_Union[_object_color_pb2.ObjectColor, _Mapping]]] = ..., hide: bool = ...) -> None: ...
