from make87_messages_ros2.rolling.sick_safetyscanners2_interfaces.msg import application_inputs_pb2 as _application_inputs_pb2
from make87_messages_ros2.rolling.sick_safetyscanners2_interfaces.msg import application_outputs_pb2 as _application_outputs_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ApplicationData(_message.Message):
    __slots__ = ("inputs", "outputs")
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    inputs: _application_inputs_pb2.ApplicationInputs
    outputs: _application_outputs_pb2.ApplicationOutputs
    def __init__(self, inputs: _Optional[_Union[_application_inputs_pb2.ApplicationInputs, _Mapping]] = ..., outputs: _Optional[_Union[_application_outputs_pb2.ApplicationOutputs, _Mapping]] = ...) -> None: ...
