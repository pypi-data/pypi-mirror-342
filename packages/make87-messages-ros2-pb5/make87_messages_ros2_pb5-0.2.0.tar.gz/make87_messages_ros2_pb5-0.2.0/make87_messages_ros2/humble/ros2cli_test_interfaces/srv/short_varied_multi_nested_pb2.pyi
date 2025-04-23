from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.ros2cli_test_interfaces.msg import short_varied_nested_pb2 as _short_varied_nested_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ShortVariedMultiNestedRequest(_message.Message):
    __slots__ = ("header", "short_varied_nested")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SHORT_VARIED_NESTED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    short_varied_nested: _short_varied_nested_pb2.ShortVariedNested
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., short_varied_nested: _Optional[_Union[_short_varied_nested_pb2.ShortVariedNested, _Mapping]] = ...) -> None: ...

class ShortVariedMultiNestedResponse(_message.Message):
    __slots__ = ("header", "bool_value")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BOOL_VALUE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    bool_value: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., bool_value: bool = ...) -> None: ...
