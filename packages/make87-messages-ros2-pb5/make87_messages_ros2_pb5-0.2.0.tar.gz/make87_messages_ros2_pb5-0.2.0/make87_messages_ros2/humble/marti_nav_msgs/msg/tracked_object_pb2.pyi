from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import duration_pb2 as _duration_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import point_pb2 as _point_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_with_covariance_pb2 as _pose_with_covariance_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import twist_with_covariance_pb2 as _twist_with_covariance_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TrackedObject(_message.Message):
    __slots__ = ("header", "ros2_header", "id", "pose", "velocity", "linear_acceleration", "linear_acceleration_covariance", "polygon", "length", "length_quality", "width", "width_quality", "classification", "classification_quality", "existence_probability", "age_duration", "prediction_duration", "active")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_FIELD_NUMBER: _ClassVar[int]
    LINEAR_ACCELERATION_FIELD_NUMBER: _ClassVar[int]
    LINEAR_ACCELERATION_COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    POLYGON_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    LENGTH_QUALITY_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    WIDTH_QUALITY_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_QUALITY_FIELD_NUMBER: _ClassVar[int]
    EXISTENCE_PROBABILITY_FIELD_NUMBER: _ClassVar[int]
    AGE_DURATION_FIELD_NUMBER: _ClassVar[int]
    PREDICTION_DURATION_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    id: int
    pose: _pose_with_covariance_pb2.PoseWithCovariance
    velocity: _twist_with_covariance_pb2.TwistWithCovariance
    linear_acceleration: _vector3_pb2.Vector3
    linear_acceleration_covariance: _containers.RepeatedScalarFieldContainer[float]
    polygon: _containers.RepeatedCompositeFieldContainer[_point_pb2.Point]
    length: float
    length_quality: float
    width: float
    width_quality: float
    classification: int
    classification_quality: float
    existence_probability: float
    age_duration: _duration_pb2.Duration
    prediction_duration: _duration_pb2.Duration
    active: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., id: _Optional[int] = ..., pose: _Optional[_Union[_pose_with_covariance_pb2.PoseWithCovariance, _Mapping]] = ..., velocity: _Optional[_Union[_twist_with_covariance_pb2.TwistWithCovariance, _Mapping]] = ..., linear_acceleration: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., linear_acceleration_covariance: _Optional[_Iterable[float]] = ..., polygon: _Optional[_Iterable[_Union[_point_pb2.Point, _Mapping]]] = ..., length: _Optional[float] = ..., length_quality: _Optional[float] = ..., width: _Optional[float] = ..., width_quality: _Optional[float] = ..., classification: _Optional[int] = ..., classification_quality: _Optional[float] = ..., existence_probability: _Optional[float] = ..., age_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., prediction_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., active: bool = ...) -> None: ...
