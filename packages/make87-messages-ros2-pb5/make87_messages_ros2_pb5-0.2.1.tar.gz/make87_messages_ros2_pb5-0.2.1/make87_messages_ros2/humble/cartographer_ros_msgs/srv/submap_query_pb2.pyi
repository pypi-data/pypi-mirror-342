from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.cartographer_ros_msgs.msg import status_response_pb2 as _status_response_pb2
from make87_messages_ros2.humble.cartographer_ros_msgs.msg import submap_texture_pb2 as _submap_texture_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SubmapQueryRequest(_message.Message):
    __slots__ = ("header", "trajectory_id", "submap_index")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TRAJECTORY_ID_FIELD_NUMBER: _ClassVar[int]
    SUBMAP_INDEX_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    trajectory_id: int
    submap_index: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., trajectory_id: _Optional[int] = ..., submap_index: _Optional[int] = ...) -> None: ...

class SubmapQueryResponse(_message.Message):
    __slots__ = ("header", "status", "submap_version", "textures")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SUBMAP_VERSION_FIELD_NUMBER: _ClassVar[int]
    TEXTURES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    status: _status_response_pb2.StatusResponse
    submap_version: int
    textures: _containers.RepeatedCompositeFieldContainer[_submap_texture_pb2.SubmapTexture]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., status: _Optional[_Union[_status_response_pb2.StatusResponse, _Mapping]] = ..., submap_version: _Optional[int] = ..., textures: _Optional[_Iterable[_Union[_submap_texture_pb2.SubmapTexture, _Mapping]]] = ...) -> None: ...
