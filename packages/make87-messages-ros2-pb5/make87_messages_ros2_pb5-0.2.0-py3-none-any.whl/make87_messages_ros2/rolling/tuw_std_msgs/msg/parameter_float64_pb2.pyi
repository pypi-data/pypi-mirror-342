from make87_messages_ros2.rolling.std_msgs.msg import string_pb2 as _string_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ParameterFloat64(_message.Message):
    __slots__ = ("name", "data")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    name: _string_pb2.String
    data: float
    def __init__(self, name: _Optional[_Union[_string_pb2.String, _Mapping]] = ..., data: _Optional[float] = ...) -> None: ...
