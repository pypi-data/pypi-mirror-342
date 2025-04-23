from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rtabmap_msgs.msg import camera_model_pb2 as _camera_model_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CameraModels(_message.Message):
    __slots__ = ("header", "models")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MODELS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    models: _containers.RepeatedCompositeFieldContainer[_camera_model_pb2.CameraModel]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., models: _Optional[_Iterable[_Union[_camera_model_pb2.CameraModel, _Mapping]]] = ...) -> None: ...
