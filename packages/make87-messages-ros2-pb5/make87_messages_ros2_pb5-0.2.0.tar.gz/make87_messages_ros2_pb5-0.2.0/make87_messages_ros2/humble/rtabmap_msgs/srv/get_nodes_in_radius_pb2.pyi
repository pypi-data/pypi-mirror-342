from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetNodesInRadiusRequest(_message.Message):
    __slots__ = ("header", "node_id", "x", "y", "z", "radius", "k")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    RADIUS_FIELD_NUMBER: _ClassVar[int]
    K_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    node_id: int
    x: float
    y: float
    z: float
    radius: float
    k: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., node_id: _Optional[int] = ..., x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ..., radius: _Optional[float] = ..., k: _Optional[int] = ...) -> None: ...

class GetNodesInRadiusResponse(_message.Message):
    __slots__ = ("header", "ids", "poses", "dists_sqr")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    IDS_FIELD_NUMBER: _ClassVar[int]
    POSES_FIELD_NUMBER: _ClassVar[int]
    DISTS_SQR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ids: _containers.RepeatedScalarFieldContainer[int]
    poses: _containers.RepeatedCompositeFieldContainer[_pose_pb2.Pose]
    dists_sqr: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ids: _Optional[_Iterable[int]] = ..., poses: _Optional[_Iterable[_Union[_pose_pb2.Pose, _Mapping]]] = ..., dists_sqr: _Optional[_Iterable[float]] = ...) -> None: ...
