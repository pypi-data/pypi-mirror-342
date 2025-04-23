from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LaneletMapBin(_message.Message):
    __slots__ = ("header", "version_map_format", "version_map", "name_map", "data")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VERSION_MAP_FORMAT_FIELD_NUMBER: _ClassVar[int]
    VERSION_MAP_FIELD_NUMBER: _ClassVar[int]
    NAME_MAP_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    version_map_format: str
    version_map: str
    name_map: str
    data: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., version_map_format: _Optional[str] = ..., version_map: _Optional[str] = ..., name_map: _Optional[str] = ..., data: _Optional[_Iterable[int]] = ...) -> None: ...
