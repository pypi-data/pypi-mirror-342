from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SmaccContainerStructure(_message.Message):
    __slots__ = ("header", "ros2_header", "path", "children", "internal_outcomes", "outcomes_from", "outcomes_to", "container_outcomes")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    CHILDREN_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_OUTCOMES_FIELD_NUMBER: _ClassVar[int]
    OUTCOMES_FROM_FIELD_NUMBER: _ClassVar[int]
    OUTCOMES_TO_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_OUTCOMES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    path: str
    children: _containers.RepeatedScalarFieldContainer[str]
    internal_outcomes: _containers.RepeatedScalarFieldContainer[str]
    outcomes_from: _containers.RepeatedScalarFieldContainer[str]
    outcomes_to: _containers.RepeatedScalarFieldContainer[str]
    container_outcomes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., path: _Optional[str] = ..., children: _Optional[_Iterable[str]] = ..., internal_outcomes: _Optional[_Iterable[str]] = ..., outcomes_from: _Optional[_Iterable[str]] = ..., outcomes_to: _Optional[_Iterable[str]] = ..., container_outcomes: _Optional[_Iterable[str]] = ...) -> None: ...
