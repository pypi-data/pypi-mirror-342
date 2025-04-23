from make87_messages_ros2.jazzy.radar_msgs.msg import radar_track_pb2 as _radar_track_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RadarTracks(_message.Message):
    __slots__ = ("header", "tracks")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TRACKS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    tracks: _containers.RepeatedCompositeFieldContainer[_radar_track_pb2.RadarTrack]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., tracks: _Optional[_Iterable[_Union[_radar_track_pb2.RadarTrack, _Mapping]]] = ...) -> None: ...
