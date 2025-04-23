from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.psdk_interfaces.msg import hms_info_msg_pb2 as _hms_info_msg_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HmsInfoTable(_message.Message):
    __slots__ = ("header", "num_msg", "table")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NUM_MSG_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    num_msg: int
    table: _containers.RepeatedCompositeFieldContainer[_hms_info_msg_pb2.HmsInfoMsg]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., num_msg: _Optional[int] = ..., table: _Optional[_Iterable[_Union[_hms_info_msg_pb2.HmsInfoMsg, _Mapping]]] = ...) -> None: ...
