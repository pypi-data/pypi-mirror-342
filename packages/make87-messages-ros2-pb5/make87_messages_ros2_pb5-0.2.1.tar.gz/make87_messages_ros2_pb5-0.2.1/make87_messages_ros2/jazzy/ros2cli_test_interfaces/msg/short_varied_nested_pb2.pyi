from make87_messages_ros2.jazzy.ros2cli_test_interfaces.msg import short_varied_pb2 as _short_varied_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ShortVariedNested(_message.Message):
    __slots__ = ("short_varied",)
    SHORT_VARIED_FIELD_NUMBER: _ClassVar[int]
    short_varied: _short_varied_pb2.ShortVaried
    def __init__(self, short_varied: _Optional[_Union[_short_varied_pb2.ShortVaried, _Mapping]] = ...) -> None: ...
