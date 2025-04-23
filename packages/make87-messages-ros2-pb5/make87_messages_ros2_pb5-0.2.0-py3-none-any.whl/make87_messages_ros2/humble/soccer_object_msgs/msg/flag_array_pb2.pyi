from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.soccer_object_msgs.msg import flag_pb2 as _flag_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FlagArray(_message.Message):
    __slots__ = ("header", "flags")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    flags: _containers.RepeatedCompositeFieldContainer[_flag_pb2.Flag]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., flags: _Optional[_Iterable[_Union[_flag_pb2.Flag, _Mapping]]] = ...) -> None: ...
