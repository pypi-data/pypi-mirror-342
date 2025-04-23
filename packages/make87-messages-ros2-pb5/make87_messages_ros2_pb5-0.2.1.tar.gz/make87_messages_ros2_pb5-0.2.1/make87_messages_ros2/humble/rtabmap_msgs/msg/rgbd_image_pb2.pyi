from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rtabmap_msgs.msg import global_descriptor_pb2 as _global_descriptor_pb2
from make87_messages_ros2.humble.rtabmap_msgs.msg import key_point_pb2 as _key_point_pb2
from make87_messages_ros2.humble.rtabmap_msgs.msg import point3f_pb2 as _point3f_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import camera_info_pb2 as _camera_info_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import compressed_image_pb2 as _compressed_image_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import image_pb2 as _image_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RGBDImage(_message.Message):
    __slots__ = ("header", "ros2_header", "rgb_camera_info", "depth_camera_info", "rgb", "depth", "rgb_compressed", "depth_compressed", "key_points", "points", "descriptors", "global_descriptor")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    RGB_CAMERA_INFO_FIELD_NUMBER: _ClassVar[int]
    DEPTH_CAMERA_INFO_FIELD_NUMBER: _ClassVar[int]
    RGB_FIELD_NUMBER: _ClassVar[int]
    DEPTH_FIELD_NUMBER: _ClassVar[int]
    RGB_COMPRESSED_FIELD_NUMBER: _ClassVar[int]
    DEPTH_COMPRESSED_FIELD_NUMBER: _ClassVar[int]
    KEY_POINTS_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTORS_FIELD_NUMBER: _ClassVar[int]
    GLOBAL_DESCRIPTOR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    rgb_camera_info: _camera_info_pb2.CameraInfo
    depth_camera_info: _camera_info_pb2.CameraInfo
    rgb: _image_pb2.Image
    depth: _image_pb2.Image
    rgb_compressed: _compressed_image_pb2.CompressedImage
    depth_compressed: _compressed_image_pb2.CompressedImage
    key_points: _containers.RepeatedCompositeFieldContainer[_key_point_pb2.KeyPoint]
    points: _containers.RepeatedCompositeFieldContainer[_point3f_pb2.Point3f]
    descriptors: _containers.RepeatedScalarFieldContainer[int]
    global_descriptor: _global_descriptor_pb2.GlobalDescriptor
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., rgb_camera_info: _Optional[_Union[_camera_info_pb2.CameraInfo, _Mapping]] = ..., depth_camera_info: _Optional[_Union[_camera_info_pb2.CameraInfo, _Mapping]] = ..., rgb: _Optional[_Union[_image_pb2.Image, _Mapping]] = ..., depth: _Optional[_Union[_image_pb2.Image, _Mapping]] = ..., rgb_compressed: _Optional[_Union[_compressed_image_pb2.CompressedImage, _Mapping]] = ..., depth_compressed: _Optional[_Union[_compressed_image_pb2.CompressedImage, _Mapping]] = ..., key_points: _Optional[_Iterable[_Union[_key_point_pb2.KeyPoint, _Mapping]]] = ..., points: _Optional[_Iterable[_Union[_point3f_pb2.Point3f, _Mapping]]] = ..., descriptors: _Optional[_Iterable[int]] = ..., global_descriptor: _Optional[_Union[_global_descriptor_pb2.GlobalDescriptor, _Mapping]] = ...) -> None: ...
