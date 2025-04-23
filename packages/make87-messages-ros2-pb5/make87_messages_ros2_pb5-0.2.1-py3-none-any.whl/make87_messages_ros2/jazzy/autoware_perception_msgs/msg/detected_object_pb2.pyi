from make87_messages_ros2.jazzy.autoware_perception_msgs.msg import detected_object_kinematics_pb2 as _detected_object_kinematics_pb2
from make87_messages_ros2.jazzy.autoware_perception_msgs.msg import object_classification_pb2 as _object_classification_pb2
from make87_messages_ros2.jazzy.autoware_perception_msgs.msg import shape_pb2 as _shape_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DetectedObject(_message.Message):
    __slots__ = ("existence_probability", "classification", "kinematics", "shape")
    EXISTENCE_PROBABILITY_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_FIELD_NUMBER: _ClassVar[int]
    KINEMATICS_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    existence_probability: float
    classification: _containers.RepeatedCompositeFieldContainer[_object_classification_pb2.ObjectClassification]
    kinematics: _detected_object_kinematics_pb2.DetectedObjectKinematics
    shape: _shape_pb2.Shape
    def __init__(self, existence_probability: _Optional[float] = ..., classification: _Optional[_Iterable[_Union[_object_classification_pb2.ObjectClassification, _Mapping]]] = ..., kinematics: _Optional[_Union[_detected_object_kinematics_pb2.DetectedObjectKinematics, _Mapping]] = ..., shape: _Optional[_Union[_shape_pb2.Shape, _Mapping]] = ...) -> None: ...
