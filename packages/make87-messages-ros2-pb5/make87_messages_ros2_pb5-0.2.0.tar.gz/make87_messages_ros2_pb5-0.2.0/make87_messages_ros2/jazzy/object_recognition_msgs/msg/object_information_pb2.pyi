from make87_messages_ros2.jazzy.sensor_msgs.msg import point_cloud2_pb2 as _point_cloud2_pb2
from make87_messages_ros2.jazzy.shape_msgs.msg import mesh_pb2 as _mesh_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ObjectInformation(_message.Message):
    __slots__ = ("name", "ground_truth_mesh", "ground_truth_point_cloud")
    NAME_FIELD_NUMBER: _ClassVar[int]
    GROUND_TRUTH_MESH_FIELD_NUMBER: _ClassVar[int]
    GROUND_TRUTH_POINT_CLOUD_FIELD_NUMBER: _ClassVar[int]
    name: str
    ground_truth_mesh: _mesh_pb2.Mesh
    ground_truth_point_cloud: _point_cloud2_pb2.PointCloud2
    def __init__(self, name: _Optional[str] = ..., ground_truth_mesh: _Optional[_Union[_mesh_pb2.Mesh, _Mapping]] = ..., ground_truth_point_cloud: _Optional[_Union[_point_cloud2_pb2.PointCloud2, _Mapping]] = ...) -> None: ...
