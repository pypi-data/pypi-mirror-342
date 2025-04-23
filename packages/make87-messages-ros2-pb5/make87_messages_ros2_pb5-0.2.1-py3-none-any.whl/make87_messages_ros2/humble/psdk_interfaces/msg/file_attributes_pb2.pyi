from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FileAttributes(_message.Message):
    __slots__ = ("header", "photo_ratio", "photo_rotation", "video_duration", "video_frame_rate", "video_rotation", "video_resolution")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PHOTO_RATIO_FIELD_NUMBER: _ClassVar[int]
    PHOTO_ROTATION_FIELD_NUMBER: _ClassVar[int]
    VIDEO_DURATION_FIELD_NUMBER: _ClassVar[int]
    VIDEO_FRAME_RATE_FIELD_NUMBER: _ClassVar[int]
    VIDEO_ROTATION_FIELD_NUMBER: _ClassVar[int]
    VIDEO_RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    photo_ratio: int
    photo_rotation: int
    video_duration: int
    video_frame_rate: int
    video_rotation: int
    video_resolution: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., photo_ratio: _Optional[int] = ..., photo_rotation: _Optional[int] = ..., video_duration: _Optional[int] = ..., video_frame_rate: _Optional[int] = ..., video_rotation: _Optional[int] = ..., video_resolution: _Optional[int] = ...) -> None: ...
