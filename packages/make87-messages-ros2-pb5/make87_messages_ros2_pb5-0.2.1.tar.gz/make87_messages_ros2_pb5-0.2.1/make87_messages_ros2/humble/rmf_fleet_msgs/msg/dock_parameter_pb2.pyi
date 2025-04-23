from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_fleet_msgs.msg import location_pb2 as _location_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DockParameter(_message.Message):
    __slots__ = ("header", "start", "finish", "path")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    FINISH_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    start: str
    finish: str
    path: _containers.RepeatedCompositeFieldContainer[_location_pb2.Location]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., start: _Optional[str] = ..., finish: _Optional[str] = ..., path: _Optional[_Iterable[_Union[_location_pb2.Location, _Mapping]]] = ...) -> None: ...
