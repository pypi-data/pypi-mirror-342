from make87_messages_ros2.rolling.geometry_msgs.msg import point_pb2 as _point_pb2
from make87_messages_ros2.rolling.geometry_msgs.msg import pose_with_covariance_stamped_pb2 as _pose_with_covariance_stamped_pb2
from make87_messages_ros2.rolling.object_recognition_msgs.msg import object_type_pb2 as _object_type_pb2
from make87_messages_ros2.rolling.sensor_msgs.msg import point_cloud2_pb2 as _point_cloud2_pb2
from make87_messages_ros2.rolling.shape_msgs.msg import mesh_pb2 as _mesh_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RecognizedObject(_message.Message):
    __slots__ = ("header", "type", "confidence", "point_clouds", "bounding_mesh", "bounding_contours", "pose")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    POINT_CLOUDS_FIELD_NUMBER: _ClassVar[int]
    BOUNDING_MESH_FIELD_NUMBER: _ClassVar[int]
    BOUNDING_CONTOURS_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    type: _object_type_pb2.ObjectType
    confidence: float
    point_clouds: _containers.RepeatedCompositeFieldContainer[_point_cloud2_pb2.PointCloud2]
    bounding_mesh: _mesh_pb2.Mesh
    bounding_contours: _containers.RepeatedCompositeFieldContainer[_point_pb2.Point]
    pose: _pose_with_covariance_stamped_pb2.PoseWithCovarianceStamped
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., type: _Optional[_Union[_object_type_pb2.ObjectType, _Mapping]] = ..., confidence: _Optional[float] = ..., point_clouds: _Optional[_Iterable[_Union[_point_cloud2_pb2.PointCloud2, _Mapping]]] = ..., bounding_mesh: _Optional[_Union[_mesh_pb2.Mesh, _Mapping]] = ..., bounding_contours: _Optional[_Iterable[_Union[_point_pb2.Point, _Mapping]]] = ..., pose: _Optional[_Union[_pose_with_covariance_stamped_pb2.PoseWithCovarianceStamped, _Mapping]] = ...) -> None: ...
