from make87_messages_ros2.rolling.geometry_msgs.msg import point_pb2 as _point_pb2
from make87_messages_ros2.rolling.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.rolling.unique_identifier_msgs.msg import uuid_pb2 as _uuid_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RadarTrack(_message.Message):
    __slots__ = ("uuid", "position", "velocity", "acceleration", "size", "classification", "position_covariance", "velocity_covariance", "acceleration_covariance", "size_covariance")
    UUID_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_FIELD_NUMBER: _ClassVar[int]
    ACCELERATION_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_FIELD_NUMBER: _ClassVar[int]
    POSITION_COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    ACCELERATION_COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    SIZE_COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    uuid: _uuid_pb2.UUID
    position: _point_pb2.Point
    velocity: _vector3_pb2.Vector3
    acceleration: _vector3_pb2.Vector3
    size: _vector3_pb2.Vector3
    classification: int
    position_covariance: _containers.RepeatedScalarFieldContainer[float]
    velocity_covariance: _containers.RepeatedScalarFieldContainer[float]
    acceleration_covariance: _containers.RepeatedScalarFieldContainer[float]
    size_covariance: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, uuid: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., position: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., velocity: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., acceleration: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., size: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., classification: _Optional[int] = ..., position_covariance: _Optional[_Iterable[float]] = ..., velocity_covariance: _Optional[_Iterable[float]] = ..., acceleration_covariance: _Optional[_Iterable[float]] = ..., size_covariance: _Optional[_Iterable[float]] = ...) -> None: ...
