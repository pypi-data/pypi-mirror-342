from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.sick_safevisionary_interfaces.msg import roi_observation_result_data_pb2 as _roi_observation_result_data_pb2
from make87_messages_ros2.humble.sick_safevisionary_interfaces.msg import roi_observation_safety_data_pb2 as _roi_observation_safety_data_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ROI(_message.Message):
    __slots__ = ("header", "id", "result_data", "safety_data", "distance_value")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    RESULT_DATA_FIELD_NUMBER: _ClassVar[int]
    SAFETY_DATA_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_VALUE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    id: int
    result_data: _roi_observation_result_data_pb2.ROIObservationResultData
    safety_data: _roi_observation_safety_data_pb2.ROIObservationSafetyData
    distance_value: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., id: _Optional[int] = ..., result_data: _Optional[_Union[_roi_observation_result_data_pb2.ROIObservationResultData, _Mapping]] = ..., safety_data: _Optional[_Union[_roi_observation_safety_data_pb2.ROIObservationSafetyData, _Mapping]] = ..., distance_value: _Optional[int] = ...) -> None: ...
