from make87_messages_ros2.jazzy.cartographer_ros_msgs.msg import histogram_bucket_pb2 as _histogram_bucket_pb2
from make87_messages_ros2.jazzy.cartographer_ros_msgs.msg import metric_label_pb2 as _metric_label_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Metric(_message.Message):
    __slots__ = ["type", "labels", "value", "counts_by_bucket"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    COUNTS_BY_BUCKET_FIELD_NUMBER: _ClassVar[int]
    type: int
    labels: _containers.RepeatedCompositeFieldContainer[_metric_label_pb2.MetricLabel]
    value: float
    counts_by_bucket: _containers.RepeatedCompositeFieldContainer[_histogram_bucket_pb2.HistogramBucket]
    def __init__(self, type: _Optional[int] = ..., labels: _Optional[_Iterable[_Union[_metric_label_pb2.MetricLabel, _Mapping]]] = ..., value: _Optional[float] = ..., counts_by_bucket: _Optional[_Iterable[_Union[_histogram_bucket_pb2.HistogramBucket, _Mapping]]] = ...) -> None: ...
