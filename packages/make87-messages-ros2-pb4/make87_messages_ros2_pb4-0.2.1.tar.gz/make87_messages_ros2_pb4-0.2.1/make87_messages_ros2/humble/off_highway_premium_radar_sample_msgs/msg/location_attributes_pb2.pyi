from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.humble.off_highway_premium_radar_sample_msgs.msg import location_attributes_header_pb2 as _location_attributes_header_pb2
from make87_messages_ros2.humble.off_highway_premium_radar_sample_msgs.msg import location_attributes_packet_pb2 as _location_attributes_packet_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LocationAttributes(_message.Message):
    __slots__ = ["header", "ros2_header", "location_attributes_header", "location_attributes_packet", "mounting_pose"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    LOCATION_ATTRIBUTES_HEADER_FIELD_NUMBER: _ClassVar[int]
    LOCATION_ATTRIBUTES_PACKET_FIELD_NUMBER: _ClassVar[int]
    MOUNTING_POSE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    location_attributes_header: _location_attributes_header_pb2.LocationAttributesHeader
    location_attributes_packet: _location_attributes_packet_pb2.LocationAttributesPacket
    mounting_pose: _pose_pb2.Pose
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., location_attributes_header: _Optional[_Union[_location_attributes_header_pb2.LocationAttributesHeader, _Mapping]] = ..., location_attributes_packet: _Optional[_Union[_location_attributes_packet_pb2.LocationAttributesPacket, _Mapping]] = ..., mounting_pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ...) -> None: ...
