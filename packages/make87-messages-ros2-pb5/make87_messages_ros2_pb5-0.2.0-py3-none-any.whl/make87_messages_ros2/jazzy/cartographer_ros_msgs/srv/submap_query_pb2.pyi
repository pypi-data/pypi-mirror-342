from make87_messages_ros2.jazzy.cartographer_ros_msgs.msg import status_response_pb2 as _status_response_pb2
from make87_messages_ros2.jazzy.cartographer_ros_msgs.msg import submap_texture_pb2 as _submap_texture_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SubmapQueryRequest(_message.Message):
    __slots__ = ("trajectory_id", "submap_index")
    TRAJECTORY_ID_FIELD_NUMBER: _ClassVar[int]
    SUBMAP_INDEX_FIELD_NUMBER: _ClassVar[int]
    trajectory_id: int
    submap_index: int
    def __init__(self, trajectory_id: _Optional[int] = ..., submap_index: _Optional[int] = ...) -> None: ...

class SubmapQueryResponse(_message.Message):
    __slots__ = ("status", "submap_version", "textures")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SUBMAP_VERSION_FIELD_NUMBER: _ClassVar[int]
    TEXTURES_FIELD_NUMBER: _ClassVar[int]
    status: _status_response_pb2.StatusResponse
    submap_version: int
    textures: _containers.RepeatedCompositeFieldContainer[_submap_texture_pb2.SubmapTexture]
    def __init__(self, status: _Optional[_Union[_status_response_pb2.StatusResponse, _Mapping]] = ..., submap_version: _Optional[int] = ..., textures: _Optional[_Iterable[_Union[_submap_texture_pb2.SubmapTexture, _Mapping]]] = ...) -> None: ...
