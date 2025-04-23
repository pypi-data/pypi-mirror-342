from make87_messages_ros2.jazzy.diagnostic_msgs.msg import key_value_pb2 as _key_value_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CalculateWhiteBalanceRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CalculateWhiteBalanceResponse(_message.Message):
    __slots__ = ("is_successful", "balance_ratios")
    IS_SUCCESSFUL_FIELD_NUMBER: _ClassVar[int]
    BALANCE_RATIOS_FIELD_NUMBER: _ClassVar[int]
    is_successful: bool
    balance_ratios: _containers.RepeatedCompositeFieldContainer[_key_value_pb2.KeyValue]
    def __init__(self, is_successful: bool = ..., balance_ratios: _Optional[_Iterable[_Union[_key_value_pb2.KeyValue, _Mapping]]] = ...) -> None: ...
