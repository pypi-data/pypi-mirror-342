from make87_messages_ros2.rolling.rmf_fleet_msgs.msg import location_pb2 as _location_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DockParameter(_message.Message):
    __slots__ = ("start", "finish", "path")
    START_FIELD_NUMBER: _ClassVar[int]
    FINISH_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    start: str
    finish: str
    path: _containers.RepeatedCompositeFieldContainer[_location_pb2.Location]
    def __init__(self, start: _Optional[str] = ..., finish: _Optional[str] = ..., path: _Optional[_Iterable[_Union[_location_pb2.Location, _Mapping]]] = ...) -> None: ...
