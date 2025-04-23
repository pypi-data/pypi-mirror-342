from make87_messages_ros2.rolling.rc_common_msgs.msg import return_code_pb2 as _return_code_pb2
from make87_messages_ros2.rolling.rc_reason_msgs.msg import load_carrier_model_pb2 as _load_carrier_model_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetLoadCarriersRequest(_message.Message):
    __slots__ = ("load_carrier_ids",)
    LOAD_CARRIER_IDS_FIELD_NUMBER: _ClassVar[int]
    load_carrier_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, load_carrier_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class GetLoadCarriersResponse(_message.Message):
    __slots__ = ("load_carriers", "return_code")
    LOAD_CARRIERS_FIELD_NUMBER: _ClassVar[int]
    RETURN_CODE_FIELD_NUMBER: _ClassVar[int]
    load_carriers: _containers.RepeatedCompositeFieldContainer[_load_carrier_model_pb2.LoadCarrierModel]
    return_code: _return_code_pb2.ReturnCode
    def __init__(self, load_carriers: _Optional[_Iterable[_Union[_load_carrier_model_pb2.LoadCarrierModel, _Mapping]]] = ..., return_code: _Optional[_Union[_return_code_pb2.ReturnCode, _Mapping]] = ...) -> None: ...
