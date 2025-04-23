from make87_messages_ros2.rolling.ur_msgs.msg import analog_pb2 as _analog_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetAnalogOutputRequest(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _analog_pb2.Analog
    def __init__(self, data: _Optional[_Union[_analog_pb2.Analog, _Mapping]] = ...) -> None: ...

class SetAnalogOutputResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
