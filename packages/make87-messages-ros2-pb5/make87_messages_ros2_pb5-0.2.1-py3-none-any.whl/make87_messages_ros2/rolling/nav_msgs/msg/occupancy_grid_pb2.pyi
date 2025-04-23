from make87_messages_ros2.rolling.nav_msgs.msg import map_meta_data_pb2 as _map_meta_data_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OccupancyGrid(_message.Message):
    __slots__ = ("header", "info", "data")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    info: _map_meta_data_pb2.MapMetaData
    data: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., info: _Optional[_Union[_map_meta_data_pb2.MapMetaData, _Mapping]] = ..., data: _Optional[_Iterable[int]] = ...) -> None: ...
