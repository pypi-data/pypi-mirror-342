from make87_messages_ros2.jazzy.rc_common_msgs.msg import return_code_pb2 as _return_code_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DeleteRegionsOfInterest2DRequest(_message.Message):
    __slots__ = ("region_of_interest_2d_ids",)
    REGION_OF_INTEREST_2D_IDS_FIELD_NUMBER: _ClassVar[int]
    region_of_interest_2d_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, region_of_interest_2d_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class DeleteRegionsOfInterest2DResponse(_message.Message):
    __slots__ = ("return_code",)
    RETURN_CODE_FIELD_NUMBER: _ClassVar[int]
    return_code: _return_code_pb2.ReturnCode
    def __init__(self, return_code: _Optional[_Union[_return_code_pb2.ReturnCode, _Mapping]] = ...) -> None: ...
