from make87_messages_ros2.rolling.rmf_traffic_msgs.msg import traffic_dependency_pb2 as _traffic_dependency_pb2
from make87_messages_ros2.rolling.rmf_traffic_msgs.msg import trajectory_pb2 as _trajectory_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Route(_message.Message):
    __slots__ = ("map", "trajectory", "checkpoints", "dependencies")
    MAP_FIELD_NUMBER: _ClassVar[int]
    TRAJECTORY_FIELD_NUMBER: _ClassVar[int]
    CHECKPOINTS_FIELD_NUMBER: _ClassVar[int]
    DEPENDENCIES_FIELD_NUMBER: _ClassVar[int]
    map: str
    trajectory: _trajectory_pb2.Trajectory
    checkpoints: _containers.RepeatedScalarFieldContainer[int]
    dependencies: _containers.RepeatedCompositeFieldContainer[_traffic_dependency_pb2.TrafficDependency]
    def __init__(self, map: _Optional[str] = ..., trajectory: _Optional[_Union[_trajectory_pb2.Trajectory, _Mapping]] = ..., checkpoints: _Optional[_Iterable[int]] = ..., dependencies: _Optional[_Iterable[_Union[_traffic_dependency_pb2.TrafficDependency, _Mapping]]] = ...) -> None: ...
