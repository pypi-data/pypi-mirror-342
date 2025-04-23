from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_stamped_pb2 as _pose_stamped_pb2
from make87_messages_ros2.humble.moveit_msgs.msg import move_it_error_codes_pb2 as _move_it_error_codes_pb2
from make87_messages_ros2.humble.moveit_msgs.msg import robot_state_pb2 as _robot_state_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetPositionFKRequest(_message.Message):
    __slots__ = ("header", "ros2_header", "fk_link_names", "robot_state")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    FK_LINK_NAMES_FIELD_NUMBER: _ClassVar[int]
    ROBOT_STATE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    fk_link_names: _containers.RepeatedScalarFieldContainer[str]
    robot_state: _robot_state_pb2.RobotState
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., fk_link_names: _Optional[_Iterable[str]] = ..., robot_state: _Optional[_Union[_robot_state_pb2.RobotState, _Mapping]] = ...) -> None: ...

class GetPositionFKResponse(_message.Message):
    __slots__ = ("header", "pose_stamped", "fk_link_names", "error_code")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    POSE_STAMPED_FIELD_NUMBER: _ClassVar[int]
    FK_LINK_NAMES_FIELD_NUMBER: _ClassVar[int]
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    pose_stamped: _containers.RepeatedCompositeFieldContainer[_pose_stamped_pb2.PoseStamped]
    fk_link_names: _containers.RepeatedScalarFieldContainer[str]
    error_code: _move_it_error_codes_pb2.MoveItErrorCodes
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., pose_stamped: _Optional[_Iterable[_Union[_pose_stamped_pb2.PoseStamped, _Mapping]]] = ..., fk_link_names: _Optional[_Iterable[str]] = ..., error_code: _Optional[_Union[_move_it_error_codes_pb2.MoveItErrorCodes, _Mapping]] = ...) -> None: ...
