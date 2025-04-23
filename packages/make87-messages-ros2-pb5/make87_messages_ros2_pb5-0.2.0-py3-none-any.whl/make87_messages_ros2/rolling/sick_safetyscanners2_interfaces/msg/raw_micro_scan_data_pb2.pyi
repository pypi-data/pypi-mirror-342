from make87_messages_ros2.rolling.sick_safetyscanners2_interfaces.msg import application_data_pb2 as _application_data_pb2
from make87_messages_ros2.rolling.sick_safetyscanners2_interfaces.msg import data_header_pb2 as _data_header_pb2
from make87_messages_ros2.rolling.sick_safetyscanners2_interfaces.msg import derived_values_pb2 as _derived_values_pb2
from make87_messages_ros2.rolling.sick_safetyscanners2_interfaces.msg import general_system_state_pb2 as _general_system_state_pb2
from make87_messages_ros2.rolling.sick_safetyscanners2_interfaces.msg import intrusion_data_pb2 as _intrusion_data_pb2
from make87_messages_ros2.rolling.sick_safetyscanners2_interfaces.msg import measurement_data_pb2 as _measurement_data_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RawMicroScanData(_message.Message):
    __slots__ = ("header", "derived_values", "general_system_state", "measurement_data", "intrusion_data", "application_data")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DERIVED_VALUES_FIELD_NUMBER: _ClassVar[int]
    GENERAL_SYSTEM_STATE_FIELD_NUMBER: _ClassVar[int]
    MEASUREMENT_DATA_FIELD_NUMBER: _ClassVar[int]
    INTRUSION_DATA_FIELD_NUMBER: _ClassVar[int]
    APPLICATION_DATA_FIELD_NUMBER: _ClassVar[int]
    header: _data_header_pb2.DataHeader
    derived_values: _derived_values_pb2.DerivedValues
    general_system_state: _general_system_state_pb2.GeneralSystemState
    measurement_data: _measurement_data_pb2.MeasurementData
    intrusion_data: _intrusion_data_pb2.IntrusionData
    application_data: _application_data_pb2.ApplicationData
    def __init__(self, header: _Optional[_Union[_data_header_pb2.DataHeader, _Mapping]] = ..., derived_values: _Optional[_Union[_derived_values_pb2.DerivedValues, _Mapping]] = ..., general_system_state: _Optional[_Union[_general_system_state_pb2.GeneralSystemState, _Mapping]] = ..., measurement_data: _Optional[_Union[_measurement_data_pb2.MeasurementData, _Mapping]] = ..., intrusion_data: _Optional[_Union[_intrusion_data_pb2.IntrusionData, _Mapping]] = ..., application_data: _Optional[_Union[_application_data_pb2.ApplicationData, _Mapping]] = ...) -> None: ...
