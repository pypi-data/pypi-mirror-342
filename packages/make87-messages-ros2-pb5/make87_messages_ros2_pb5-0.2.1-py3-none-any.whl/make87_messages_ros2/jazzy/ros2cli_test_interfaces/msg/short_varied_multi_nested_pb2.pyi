from make87_messages_ros2.jazzy.ros2cli_test_interfaces.msg import short_varied_nested_pb2 as _short_varied_nested_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ShortVariedMultiNested(_message.Message):
    __slots__ = ("short_varied_nested",)
    SHORT_VARIED_NESTED_FIELD_NUMBER: _ClassVar[int]
    short_varied_nested: _short_varied_nested_pb2.ShortVariedNested
    def __init__(self, short_varied_nested: _Optional[_Union[_short_varied_nested_pb2.ShortVariedNested, _Mapping]] = ...) -> None: ...
