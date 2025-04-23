from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CostmapFilterInfo(_message.Message):
    __slots__ = ("header", "type", "filter_mask_topic", "base", "multiplier")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    FILTER_MASK_TOPIC_FIELD_NUMBER: _ClassVar[int]
    BASE_FIELD_NUMBER: _ClassVar[int]
    MULTIPLIER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    type: int
    filter_mask_topic: str
    base: float
    multiplier: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., type: _Optional[int] = ..., filter_mask_topic: _Optional[str] = ..., base: _Optional[float] = ..., multiplier: _Optional[float] = ...) -> None: ...
