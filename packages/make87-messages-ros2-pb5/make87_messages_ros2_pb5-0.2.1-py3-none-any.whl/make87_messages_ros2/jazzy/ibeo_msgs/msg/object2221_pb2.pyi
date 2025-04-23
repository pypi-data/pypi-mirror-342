from make87_messages_ros2.jazzy.ibeo_msgs.msg import point2_di_pb2 as _point2_di_pb2
from make87_messages_ros2.jazzy.ibeo_msgs.msg import size2_d_pb2 as _size2_d_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Object2221(_message.Message):
    __slots__ = ("id", "age", "prediction_age", "relative_timestamp", "reference_point", "reference_point_sigma", "closest_point", "bounding_box_center", "bounding_box_width", "bounding_box_length", "object_box_center", "object_box_size", "object_box_orientation", "absolute_velocity", "absolute_velocity_sigma", "relative_velocity", "classification", "classification_age", "classification_certainty", "number_of_contour_points", "contour_point_list")
    ID_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    PREDICTION_AGE_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_POINT_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_POINT_SIGMA_FIELD_NUMBER: _ClassVar[int]
    CLOSEST_POINT_FIELD_NUMBER: _ClassVar[int]
    BOUNDING_BOX_CENTER_FIELD_NUMBER: _ClassVar[int]
    BOUNDING_BOX_WIDTH_FIELD_NUMBER: _ClassVar[int]
    BOUNDING_BOX_LENGTH_FIELD_NUMBER: _ClassVar[int]
    OBJECT_BOX_CENTER_FIELD_NUMBER: _ClassVar[int]
    OBJECT_BOX_SIZE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_BOX_ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_VELOCITY_SIGMA_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_AGE_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_CERTAINTY_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_CONTOUR_POINTS_FIELD_NUMBER: _ClassVar[int]
    CONTOUR_POINT_LIST_FIELD_NUMBER: _ClassVar[int]
    id: int
    age: int
    prediction_age: int
    relative_timestamp: int
    reference_point: _point2_di_pb2.Point2Di
    reference_point_sigma: _point2_di_pb2.Point2Di
    closest_point: _point2_di_pb2.Point2Di
    bounding_box_center: _point2_di_pb2.Point2Di
    bounding_box_width: int
    bounding_box_length: int
    object_box_center: _point2_di_pb2.Point2Di
    object_box_size: _size2_d_pb2.Size2D
    object_box_orientation: int
    absolute_velocity: _point2_di_pb2.Point2Di
    absolute_velocity_sigma: _size2_d_pb2.Size2D
    relative_velocity: _point2_di_pb2.Point2Di
    classification: int
    classification_age: int
    classification_certainty: int
    number_of_contour_points: int
    contour_point_list: _containers.RepeatedCompositeFieldContainer[_point2_di_pb2.Point2Di]
    def __init__(self, id: _Optional[int] = ..., age: _Optional[int] = ..., prediction_age: _Optional[int] = ..., relative_timestamp: _Optional[int] = ..., reference_point: _Optional[_Union[_point2_di_pb2.Point2Di, _Mapping]] = ..., reference_point_sigma: _Optional[_Union[_point2_di_pb2.Point2Di, _Mapping]] = ..., closest_point: _Optional[_Union[_point2_di_pb2.Point2Di, _Mapping]] = ..., bounding_box_center: _Optional[_Union[_point2_di_pb2.Point2Di, _Mapping]] = ..., bounding_box_width: _Optional[int] = ..., bounding_box_length: _Optional[int] = ..., object_box_center: _Optional[_Union[_point2_di_pb2.Point2Di, _Mapping]] = ..., object_box_size: _Optional[_Union[_size2_d_pb2.Size2D, _Mapping]] = ..., object_box_orientation: _Optional[int] = ..., absolute_velocity: _Optional[_Union[_point2_di_pb2.Point2Di, _Mapping]] = ..., absolute_velocity_sigma: _Optional[_Union[_size2_d_pb2.Size2D, _Mapping]] = ..., relative_velocity: _Optional[_Union[_point2_di_pb2.Point2Di, _Mapping]] = ..., classification: _Optional[int] = ..., classification_age: _Optional[int] = ..., classification_certainty: _Optional[int] = ..., number_of_contour_points: _Optional[int] = ..., contour_point_list: _Optional[_Iterable[_Union[_point2_di_pb2.Point2Di, _Mapping]]] = ...) -> None: ...
