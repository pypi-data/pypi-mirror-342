from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.test_interface_files.msg import basic_types_pb2 as _basic_types_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Nested(_message.Message):
    __slots__ = ("header", "basic_types_value")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BASIC_TYPES_VALUE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    basic_types_value: _basic_types_pb2.BasicTypes
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., basic_types_value: _Optional[_Union[_basic_types_pb2.BasicTypes, _Mapping]] = ...) -> None: ...
