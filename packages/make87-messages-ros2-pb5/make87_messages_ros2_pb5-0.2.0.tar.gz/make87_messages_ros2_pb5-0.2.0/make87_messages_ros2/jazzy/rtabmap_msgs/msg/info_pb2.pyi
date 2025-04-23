from make87_messages_ros2.jazzy.geometry_msgs.msg import transform_pb2 as _transform_pb2
from make87_messages_ros2.jazzy.rtabmap_msgs.msg import map_graph_pb2 as _map_graph_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Info(_message.Message):
    __slots__ = ("header", "ref_id", "loop_closure_id", "proximity_detection_id", "landmark_id", "loop_closure_transform", "wm_state", "posterior_keys", "posterior_values", "likelihood_keys", "likelihood_values", "raw_likelihood_keys", "raw_likelihood_values", "weights_keys", "weights_values", "labels_keys", "labels_values", "stats_keys", "stats_values", "local_path", "current_goal_id", "odom_cache")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    REF_ID_FIELD_NUMBER: _ClassVar[int]
    LOOP_CLOSURE_ID_FIELD_NUMBER: _ClassVar[int]
    PROXIMITY_DETECTION_ID_FIELD_NUMBER: _ClassVar[int]
    LANDMARK_ID_FIELD_NUMBER: _ClassVar[int]
    LOOP_CLOSURE_TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    WM_STATE_FIELD_NUMBER: _ClassVar[int]
    POSTERIOR_KEYS_FIELD_NUMBER: _ClassVar[int]
    POSTERIOR_VALUES_FIELD_NUMBER: _ClassVar[int]
    LIKELIHOOD_KEYS_FIELD_NUMBER: _ClassVar[int]
    LIKELIHOOD_VALUES_FIELD_NUMBER: _ClassVar[int]
    RAW_LIKELIHOOD_KEYS_FIELD_NUMBER: _ClassVar[int]
    RAW_LIKELIHOOD_VALUES_FIELD_NUMBER: _ClassVar[int]
    WEIGHTS_KEYS_FIELD_NUMBER: _ClassVar[int]
    WEIGHTS_VALUES_FIELD_NUMBER: _ClassVar[int]
    LABELS_KEYS_FIELD_NUMBER: _ClassVar[int]
    LABELS_VALUES_FIELD_NUMBER: _ClassVar[int]
    STATS_KEYS_FIELD_NUMBER: _ClassVar[int]
    STATS_VALUES_FIELD_NUMBER: _ClassVar[int]
    LOCAL_PATH_FIELD_NUMBER: _ClassVar[int]
    CURRENT_GOAL_ID_FIELD_NUMBER: _ClassVar[int]
    ODOM_CACHE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ref_id: int
    loop_closure_id: int
    proximity_detection_id: int
    landmark_id: int
    loop_closure_transform: _transform_pb2.Transform
    wm_state: _containers.RepeatedScalarFieldContainer[int]
    posterior_keys: _containers.RepeatedScalarFieldContainer[int]
    posterior_values: _containers.RepeatedScalarFieldContainer[float]
    likelihood_keys: _containers.RepeatedScalarFieldContainer[int]
    likelihood_values: _containers.RepeatedScalarFieldContainer[float]
    raw_likelihood_keys: _containers.RepeatedScalarFieldContainer[int]
    raw_likelihood_values: _containers.RepeatedScalarFieldContainer[float]
    weights_keys: _containers.RepeatedScalarFieldContainer[int]
    weights_values: _containers.RepeatedScalarFieldContainer[int]
    labels_keys: _containers.RepeatedScalarFieldContainer[int]
    labels_values: _containers.RepeatedScalarFieldContainer[str]
    stats_keys: _containers.RepeatedScalarFieldContainer[str]
    stats_values: _containers.RepeatedScalarFieldContainer[float]
    local_path: _containers.RepeatedScalarFieldContainer[int]
    current_goal_id: int
    odom_cache: _map_graph_pb2.MapGraph
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ref_id: _Optional[int] = ..., loop_closure_id: _Optional[int] = ..., proximity_detection_id: _Optional[int] = ..., landmark_id: _Optional[int] = ..., loop_closure_transform: _Optional[_Union[_transform_pb2.Transform, _Mapping]] = ..., wm_state: _Optional[_Iterable[int]] = ..., posterior_keys: _Optional[_Iterable[int]] = ..., posterior_values: _Optional[_Iterable[float]] = ..., likelihood_keys: _Optional[_Iterable[int]] = ..., likelihood_values: _Optional[_Iterable[float]] = ..., raw_likelihood_keys: _Optional[_Iterable[int]] = ..., raw_likelihood_values: _Optional[_Iterable[float]] = ..., weights_keys: _Optional[_Iterable[int]] = ..., weights_values: _Optional[_Iterable[int]] = ..., labels_keys: _Optional[_Iterable[int]] = ..., labels_values: _Optional[_Iterable[str]] = ..., stats_keys: _Optional[_Iterable[str]] = ..., stats_values: _Optional[_Iterable[float]] = ..., local_path: _Optional[_Iterable[int]] = ..., current_goal_id: _Optional[int] = ..., odom_cache: _Optional[_Union[_map_graph_pb2.MapGraph, _Mapping]] = ...) -> None: ...
