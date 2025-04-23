from make87_messages_ros2.rolling.slg_msgs.msg import segment_pb2 as _segment_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SegmentArray(_message.Message):
    __slots__ = ("header", "segments")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    segments: _containers.RepeatedCompositeFieldContainer[_segment_pb2.Segment]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., segments: _Optional[_Iterable[_Union[_segment_pb2.Segment, _Mapping]]] = ...) -> None: ...
