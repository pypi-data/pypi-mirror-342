from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.off_highway_general_purpose_radar_msgs.msg import target_a_pb2 as _target_a_pb2
from make87_messages_ros2.humble.off_highway_general_purpose_radar_msgs.msg import target_b_pb2 as _target_b_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Target(_message.Message):
    __slots__ = ("header", "ros2_header", "a", "b")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    A_FIELD_NUMBER: _ClassVar[int]
    B_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    a: _target_a_pb2.TargetA
    b: _target_b_pb2.TargetB
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., a: _Optional[_Union[_target_a_pb2.TargetA, _Mapping]] = ..., b: _Optional[_Union[_target_b_pb2.TargetB, _Mapping]] = ...) -> None: ...
