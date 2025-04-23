import common_pb2 as _common_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class HandlerInvokeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INVOKE: _ClassVar[HandlerInvokeType]
    RUN_NOW: _ClassVar[HandlerInvokeType]
    CRON_SCHEDULE: _ClassVar[HandlerInvokeType]
    RUN_INTERVAL: _ClassVar[HandlerInvokeType]
    WEBHOOK: _ClassVar[HandlerInvokeType]

class DispatchMessageType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DISPATCH_MESSAGE_TYPE_NONE: _ClassVar[DispatchMessageType]
    DISPATCH_MESSAGE_INVOKE: _ClassVar[DispatchMessageType]
    DISPATCH_MESSAGE_WORK_COMPLETED: _ClassVar[DispatchMessageType]
INVOKE: HandlerInvokeType
RUN_NOW: HandlerInvokeType
CRON_SCHEDULE: HandlerInvokeType
RUN_INTERVAL: HandlerInvokeType
WEBHOOK: HandlerInvokeType
DISPATCH_MESSAGE_TYPE_NONE: DispatchMessageType
DISPATCH_MESSAGE_INVOKE: DispatchMessageType
DISPATCH_MESSAGE_WORK_COMPLETED: DispatchMessageType

class RegisterHandlerRequest(_message.Message):
    __slots__ = ('dispatch_id', 'handler_name', 'timeout_ms', 'options')
    DISPATCH_ID_FIELD_NUMBER: _ClassVar[int]
    HANDLER_NAME_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_MS_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    dispatch_id: str
    handler_name: str
    timeout_ms: int
    options: _containers.RepeatedCompositeFieldContainer[HandlerOption]

    def __init__(self, dispatch_id: _Optional[str]=..., handler_name: _Optional[str]=..., timeout_ms: _Optional[int]=..., options: _Optional[_Iterable[_Union[HandlerOption, _Mapping]]]=...) -> None:
        ...

class HandlerInvokeOption(_message.Message):
    __slots__ = ('type', 'value')
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    type: HandlerInvokeType
    value: str

    def __init__(self, type: _Optional[_Union[HandlerInvokeType, str]]=..., value: _Optional[str]=...) -> None:
        ...

class HandlerOption(_message.Message):
    __slots__ = ('invoke',)
    INVOKE_FIELD_NUMBER: _ClassVar[int]
    invoke: HandlerInvokeOption

    def __init__(self, invoke: _Optional[_Union[HandlerInvokeOption, _Mapping]]=...) -> None:
        ...

class RegisterHandlerResponse(_message.Message):
    __slots__ = ('error', 'id')
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    error: _common_pb2.Error
    id: str

    def __init__(self, error: _Optional[_Union[_common_pb2.Error, _Mapping]]=..., id: _Optional[str]=...) -> None:
        ...

class UnregisterHandlerRequest(_message.Message):
    __slots__ = ('id',)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str

    def __init__(self, id: _Optional[str]=...) -> None:
        ...

class UnregisterHandlerResponse(_message.Message):
    __slots__ = ('error',)
    ERROR_FIELD_NUMBER: _ClassVar[int]
    error: _common_pb2.Error

    def __init__(self, error: _Optional[_Union[_common_pb2.Error, _Mapping]]=...) -> None:
        ...

class ListHandlersRequest(_message.Message):
    __slots__ = ()

    def __init__(self) -> None:
        ...

class HandlerInfo(_message.Message):
    __slots__ = ('name', 'options', 'dispatch_id', 'id', 'last_invoked_client_timestamp', 'is_active')
    NAME_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    DISPATCH_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    LAST_INVOKED_CLIENT_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    name: str
    options: _containers.RepeatedCompositeFieldContainer[HandlerOption]
    dispatch_id: str
    id: str
    last_invoked_client_timestamp: _timestamp_pb2.Timestamp
    is_active: bool

    def __init__(self, name: _Optional[str]=..., options: _Optional[_Iterable[_Union[HandlerOption, _Mapping]]]=..., dispatch_id: _Optional[str]=..., id: _Optional[str]=..., last_invoked_client_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., is_active: bool=...) -> None:
        ...

class ListHandlersResponse(_message.Message):
    __slots__ = ('error', 'handlers')
    ERROR_FIELD_NUMBER: _ClassVar[int]
    HANDLERS_FIELD_NUMBER: _ClassVar[int]
    error: _common_pb2.Error
    handlers: _containers.RepeatedCompositeFieldContainer[HandlerInfo]

    def __init__(self, error: _Optional[_Union[_common_pb2.Error, _Mapping]]=..., handlers: _Optional[_Iterable[_Union[HandlerInfo, _Mapping]]]=...) -> None:
        ...

class DispatchRequest(_message.Message):
    __slots__ = ('dispatch_id', 'client_version')
    DISPATCH_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_FIELD_NUMBER: _ClassVar[int]
    dispatch_id: str
    client_version: str

    def __init__(self, dispatch_id: _Optional[str]=..., client_version: _Optional[str]=...) -> None:
        ...

class DispatchMessage(_message.Message):
    __slots__ = ('type', 'invoke')
    TYPE_FIELD_NUMBER: _ClassVar[int]
    INVOKE_FIELD_NUMBER: _ClassVar[int]
    type: DispatchMessageType
    invoke: DispatchHandlerInvoke

    def __init__(self, type: _Optional[_Union[DispatchMessageType, str]]=..., invoke: _Optional[_Union[DispatchHandlerInvoke, _Mapping]]=...) -> None:
        ...

class DispatchHandlerInvoke(_message.Message):
    __slots__ = ('invocation_id', 'dispatch_id', 'handler_id', 'handler_name', 'timeout_ms', 'reason', 'args')

    class ArgsEntry(_message.Message):
        __slots__ = ('key', 'value')
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str

        def __init__(self, key: _Optional[str]=..., value: _Optional[str]=...) -> None:
            ...
    INVOCATION_ID_FIELD_NUMBER: _ClassVar[int]
    DISPATCH_ID_FIELD_NUMBER: _ClassVar[int]
    HANDLER_ID_FIELD_NUMBER: _ClassVar[int]
    HANDLER_NAME_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_MS_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    invocation_id: str
    dispatch_id: str
    handler_id: str
    handler_name: str
    timeout_ms: int
    reason: HandlerInvokeType
    args: _containers.ScalarMap[str, str]

    def __init__(self, invocation_id: _Optional[str]=..., dispatch_id: _Optional[str]=..., handler_id: _Optional[str]=..., handler_name: _Optional[str]=..., timeout_ms: _Optional[int]=..., reason: _Optional[_Union[HandlerInvokeType, str]]=..., args: _Optional[_Mapping[str, str]]=...) -> None:
        ...

class Log(_message.Message):
    __slots__ = ('level', 'timestamp', 'message')
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    level: str
    timestamp: _timestamp_pb2.Timestamp
    message: str

    def __init__(self, level: _Optional[str]=..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., message: _Optional[str]=...) -> None:
        ...

class ReportInvocationRequest(_message.Message):
    __slots__ = ('handler_invoke', 'start_client_timestamp', 'duration_ms', 'result', 'error', 'logs')
    HANDLER_INVOKE_FIELD_NUMBER: _ClassVar[int]
    START_CLIENT_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    LOGS_FIELD_NUMBER: _ClassVar[int]
    handler_invoke: DispatchHandlerInvoke
    start_client_timestamp: _timestamp_pb2.Timestamp
    duration_ms: int
    result: InvokeResult
    error: _common_pb2.Error
    logs: _containers.RepeatedCompositeFieldContainer[Log]

    def __init__(self, handler_invoke: _Optional[_Union[DispatchHandlerInvoke, _Mapping]]=..., start_client_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., duration_ms: _Optional[int]=..., result: _Optional[_Union[InvokeResult, _Mapping]]=..., error: _Optional[_Union[_common_pb2.Error, _Mapping]]=..., logs: _Optional[_Iterable[_Union[Log, _Mapping]]]=...) -> None:
        ...

class ReportInvocationResponse(_message.Message):
    __slots__ = ('error',)
    ERROR_FIELD_NUMBER: _ClassVar[int]
    error: _common_pb2.Error

    def __init__(self, error: _Optional[_Union[_common_pb2.Error, _Mapping]]=...) -> None:
        ...

class InvokeResult(_message.Message):
    __slots__ = ('value',)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str

    def __init__(self, value: _Optional[str]=...) -> None:
        ...

class GetHandlerHistoryRequest(_message.Message):
    __slots__ = ('handler_name', 'start_time', 'end_time', 'include_logs', 'tail')
    HANDLER_NAME_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_LOGS_FIELD_NUMBER: _ClassVar[int]
    TAIL_FIELD_NUMBER: _ClassVar[int]
    handler_name: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    include_logs: bool
    tail: int

    def __init__(self, handler_name: _Optional[str]=..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., include_logs: bool=..., tail: _Optional[int]=...) -> None:
        ...

class HandlerExecution(_message.Message):
    __slots__ = ('handler_name', 'handler_id', 'invocation_id', 'dispatch_id', 'publish_server_timestamp', 'receive_server_timestamp', 'start_client_timestamp', 'duration_ms', 'error', 'logs')
    HANDLER_NAME_FIELD_NUMBER: _ClassVar[int]
    HANDLER_ID_FIELD_NUMBER: _ClassVar[int]
    INVOCATION_ID_FIELD_NUMBER: _ClassVar[int]
    DISPATCH_ID_FIELD_NUMBER: _ClassVar[int]
    PUBLISH_SERVER_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    RECEIVE_SERVER_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    START_CLIENT_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    LOGS_FIELD_NUMBER: _ClassVar[int]
    handler_name: str
    handler_id: str
    invocation_id: str
    dispatch_id: str
    publish_server_timestamp: _timestamp_pb2.Timestamp
    receive_server_timestamp: _timestamp_pb2.Timestamp
    start_client_timestamp: _timestamp_pb2.Timestamp
    duration_ms: int
    error: _common_pb2.Error
    logs: _containers.RepeatedCompositeFieldContainer[Log]

    def __init__(self, handler_name: _Optional[str]=..., handler_id: _Optional[str]=..., invocation_id: _Optional[str]=..., dispatch_id: _Optional[str]=..., publish_server_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., receive_server_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., start_client_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., duration_ms: _Optional[int]=..., error: _Optional[_Union[_common_pb2.Error, _Mapping]]=..., logs: _Optional[_Iterable[_Union[Log, _Mapping]]]=...) -> None:
        ...

class GetHandlerHistoryResponse(_message.Message):
    __slots__ = ('error', 'history')
    ERROR_FIELD_NUMBER: _ClassVar[int]
    HISTORY_FIELD_NUMBER: _ClassVar[int]
    error: _common_pb2.Error
    history: _containers.RepeatedCompositeFieldContainer[HandlerExecution]

    def __init__(self, error: _Optional[_Union[_common_pb2.Error, _Mapping]]=..., history: _Optional[_Iterable[_Union[HandlerExecution, _Mapping]]]=...) -> None:
        ...