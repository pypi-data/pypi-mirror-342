from make87_messages_ros2.rolling.rosbridge_test_msgs.msg import test_float32_bounded_array_pb2 as _test_float32_bounded_array_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TestNestedBoundedArray(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _test_float32_bounded_array_pb2.TestFloat32BoundedArray
    def __init__(self, data: _Optional[_Union[_test_float32_bounded_array_pb2.TestFloat32BoundedArray, _Mapping]] = ...) -> None: ...
