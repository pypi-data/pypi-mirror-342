from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SmaccStatus(_message.Message):
    __slots__ = ("header", "ros2_header", "current_states", "global_variable_names", "global_variable_values")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    CURRENT_STATES_FIELD_NUMBER: _ClassVar[int]
    GLOBAL_VARIABLE_NAMES_FIELD_NUMBER: _ClassVar[int]
    GLOBAL_VARIABLE_VALUES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    current_states: _containers.RepeatedScalarFieldContainer[str]
    global_variable_names: _containers.RepeatedScalarFieldContainer[str]
    global_variable_values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., current_states: _Optional[_Iterable[str]] = ..., global_variable_names: _Optional[_Iterable[str]] = ..., global_variable_values: _Optional[_Iterable[str]] = ...) -> None: ...
