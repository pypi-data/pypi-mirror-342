from make87_messages_ros2.rolling.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.rolling.tuw_std_msgs.msg import parameter_array_pb2 as _parameter_array_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Shape(_message.Message):
    __slots__ = ("id", "shape", "type", "poses", "params_poses", "params")
    ID_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    POSES_FIELD_NUMBER: _ClassVar[int]
    PARAMS_POSES_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    id: int
    shape: int
    type: int
    poses: _containers.RepeatedCompositeFieldContainer[_pose_pb2.Pose]
    params_poses: _containers.RepeatedCompositeFieldContainer[_parameter_array_pb2.ParameterArray]
    params: _parameter_array_pb2.ParameterArray
    def __init__(self, id: _Optional[int] = ..., shape: _Optional[int] = ..., type: _Optional[int] = ..., poses: _Optional[_Iterable[_Union[_pose_pb2.Pose, _Mapping]]] = ..., params_poses: _Optional[_Iterable[_Union[_parameter_array_pb2.ParameterArray, _Mapping]]] = ..., params: _Optional[_Union[_parameter_array_pb2.ParameterArray, _Mapping]] = ...) -> None: ...
