from make87_messages_ros2.jazzy.rc_common_msgs.msg import return_code_pb2 as _return_code_pb2
from make87_messages_ros2.jazzy.rc_reason_msgs.msg import region_of_interest3_d_pb2 as _region_of_interest3_d_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetRegionsOfInterest3DRequest(_message.Message):
    __slots__ = ("region_of_interest_ids",)
    REGION_OF_INTEREST_IDS_FIELD_NUMBER: _ClassVar[int]
    region_of_interest_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, region_of_interest_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class GetRegionsOfInterest3DResponse(_message.Message):
    __slots__ = ("regions_of_interest", "return_code")
    REGIONS_OF_INTEREST_FIELD_NUMBER: _ClassVar[int]
    RETURN_CODE_FIELD_NUMBER: _ClassVar[int]
    regions_of_interest: _containers.RepeatedCompositeFieldContainer[_region_of_interest3_d_pb2.RegionOfInterest3D]
    return_code: _return_code_pb2.ReturnCode
    def __init__(self, regions_of_interest: _Optional[_Iterable[_Union[_region_of_interest3_d_pb2.RegionOfInterest3D, _Mapping]]] = ..., return_code: _Optional[_Union[_return_code_pb2.ReturnCode, _Mapping]] = ...) -> None: ...
