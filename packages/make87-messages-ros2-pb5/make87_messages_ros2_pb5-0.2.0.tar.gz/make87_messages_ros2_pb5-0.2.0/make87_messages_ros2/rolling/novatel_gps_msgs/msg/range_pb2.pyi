from make87_messages_ros2.rolling.novatel_gps_msgs.msg import novatel_message_header_pb2 as _novatel_message_header_pb2
from make87_messages_ros2.rolling.novatel_gps_msgs.msg import range_information_pb2 as _range_information_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Range(_message.Message):
    __slots__ = ("header", "novatel_msg_header", "numb_of_observ", "info")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NOVATEL_MSG_HEADER_FIELD_NUMBER: _ClassVar[int]
    NUMB_OF_OBSERV_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    novatel_msg_header: _novatel_message_header_pb2.NovatelMessageHeader
    numb_of_observ: int
    info: _containers.RepeatedCompositeFieldContainer[_range_information_pb2.RangeInformation]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., novatel_msg_header: _Optional[_Union[_novatel_message_header_pb2.NovatelMessageHeader, _Mapping]] = ..., numb_of_observ: _Optional[int] = ..., info: _Optional[_Iterable[_Union[_range_information_pb2.RangeInformation, _Mapping]]] = ...) -> None: ...
