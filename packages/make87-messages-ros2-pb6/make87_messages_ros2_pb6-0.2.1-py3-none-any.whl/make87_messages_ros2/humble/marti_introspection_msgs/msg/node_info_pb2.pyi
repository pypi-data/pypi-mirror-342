from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.marti_introspection_msgs.msg import param_info_pb2 as _param_info_pb2
from make87_messages_ros2.humble.marti_introspection_msgs.msg import service_info_pb2 as _service_info_pb2
from make87_messages_ros2.humble.marti_introspection_msgs.msg import topic_info_pb2 as _topic_info_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NodeInfo(_message.Message):
    __slots__ = ("header", "name", "location", "nodelet_manager", "description", "topics", "parameters", "services")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    NODELET_MANAGER_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TOPICS_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    SERVICES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    location: str
    nodelet_manager: str
    description: str
    topics: _containers.RepeatedCompositeFieldContainer[_topic_info_pb2.TopicInfo]
    parameters: _containers.RepeatedCompositeFieldContainer[_param_info_pb2.ParamInfo]
    services: _containers.RepeatedCompositeFieldContainer[_service_info_pb2.ServiceInfo]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., location: _Optional[str] = ..., nodelet_manager: _Optional[str] = ..., description: _Optional[str] = ..., topics: _Optional[_Iterable[_Union[_topic_info_pb2.TopicInfo, _Mapping]]] = ..., parameters: _Optional[_Iterable[_Union[_param_info_pb2.ParamInfo, _Mapping]]] = ..., services: _Optional[_Iterable[_Union[_service_info_pb2.ServiceInfo, _Mapping]]] = ...) -> None: ...
