from make87_messages_ros2.rolling.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TestTimeArray(_message.Message):
    __slots__ = ("times",)
    TIMES_FIELD_NUMBER: _ClassVar[int]
    times: _containers.RepeatedCompositeFieldContainer[_time_pb2.Time]
    def __init__(self, times: _Optional[_Iterable[_Union[_time_pb2.Time, _Mapping]]] = ...) -> None: ...
