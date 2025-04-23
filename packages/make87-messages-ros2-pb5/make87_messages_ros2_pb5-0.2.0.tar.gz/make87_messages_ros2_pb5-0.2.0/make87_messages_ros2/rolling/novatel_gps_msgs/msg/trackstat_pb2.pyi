from make87_messages_ros2.rolling.novatel_gps_msgs.msg import trackstat_channel_pb2 as _trackstat_channel_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Trackstat(_message.Message):
    __slots__ = ("header", "solution_status", "position_type", "cutoff", "channels")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SOLUTION_STATUS_FIELD_NUMBER: _ClassVar[int]
    POSITION_TYPE_FIELD_NUMBER: _ClassVar[int]
    CUTOFF_FIELD_NUMBER: _ClassVar[int]
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    solution_status: str
    position_type: str
    cutoff: float
    channels: _containers.RepeatedCompositeFieldContainer[_trackstat_channel_pb2.TrackstatChannel]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., solution_status: _Optional[str] = ..., position_type: _Optional[str] = ..., cutoff: _Optional[float] = ..., channels: _Optional[_Iterable[_Union[_trackstat_channel_pb2.TrackstatChannel, _Mapping]]] = ...) -> None: ...
