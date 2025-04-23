"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 28, 1, '', 'cortex-axon-agent.proto')
_sym_db = _symbol_database.Default()
from . import common_pb2 as common__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17cortex-axon-agent.proto\x12\x0bcortex.axon\x1a\x0ccommon.proto\x1a\x1fgoogle/protobuf/timestamp.proto"\x84\x01\n\x16RegisterHandlerRequest\x12\x13\n\x0bdispatch_id\x18\x01 \x01(\t\x12\x14\n\x0chandler_name\x18\x02 \x01(\t\x12\x12\n\ntimeout_ms\x18\x03 \x01(\x05\x12+\n\x07options\x18\x04 \x03(\x0b2\x1a.cortex.axon.HandlerOption"R\n\x13HandlerInvokeOption\x12,\n\x04type\x18\x01 \x01(\x0e2\x1e.cortex.axon.HandlerInvokeType\x12\r\n\x05value\x18\x02 \x01(\t"M\n\rHandlerOption\x122\n\x06invoke\x18\x01 \x01(\x0b2 .cortex.axon.HandlerInvokeOptionH\x00B\x08\n\x06option"H\n\x17RegisterHandlerResponse\x12!\n\x05error\x18\x01 \x01(\x0b2\x12.cortex.axon.Error\x12\n\n\x02id\x18\x02 \x01(\t"&\n\x18UnregisterHandlerRequest\x12\n\n\x02id\x18\x01 \x01(\t">\n\x19UnregisterHandlerResponse\x12!\n\x05error\x18\x01 \x01(\x0b2\x12.cortex.axon.Error"\x15\n\x13ListHandlersRequest"\xbf\x01\n\x0bHandlerInfo\x12\x0c\n\x04name\x18\x01 \x01(\t\x12+\n\x07options\x18\x02 \x03(\x0b2\x1a.cortex.axon.HandlerOption\x12\x13\n\x0bdispatch_id\x18\x14 \x01(\t\x12\n\n\x02id\x18\x15 \x01(\t\x12A\n\x1dlast_invoked_client_timestamp\x18d \x01(\x0b2\x1a.google.protobuf.Timestamp\x12\x11\n\tis_active\x18e \x01(\x08"e\n\x14ListHandlersResponse\x12!\n\x05error\x18\x01 \x01(\x0b2\x12.cortex.axon.Error\x12*\n\x08handlers\x18\x02 \x03(\x0b2\x18.cortex.axon.HandlerInfo">\n\x0fDispatchRequest\x12\x13\n\x0bdispatch_id\x18\x01 \x01(\t\x12\x16\n\x0eclient_version\x18\x02 \x01(\t"\x82\x01\n\x0fDispatchMessage\x12.\n\x04type\x18\x01 \x01(\x0e2 .cortex.axon.DispatchMessageType\x124\n\x06invoke\x18\n \x01(\x0b2".cortex.axon.DispatchHandlerInvokeH\x00B\t\n\x07message"\x9a\x02\n\x15DispatchHandlerInvoke\x12\x15\n\rinvocation_id\x18\x01 \x01(\t\x12\x13\n\x0bdispatch_id\x18\x02 \x01(\t\x12\x12\n\nhandler_id\x18\x03 \x01(\t\x12\x14\n\x0chandler_name\x18\x04 \x01(\t\x12\x12\n\ntimeout_ms\x18\n \x01(\x05\x12.\n\x06reason\x18\x0b \x01(\x0e2\x1e.cortex.axon.HandlerInvokeType\x12:\n\x04args\x18\x14 \x03(\x0b2,.cortex.axon.DispatchHandlerInvoke.ArgsEntry\x1a+\n\tArgsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x028\x01"T\n\x03Log\x12\r\n\x05level\x18\x01 \x01(\t\x12-\n\ttimestamp\x18\x02 \x01(\x0b2\x1a.google.protobuf.Timestamp\x12\x0f\n\x07message\x18\x03 \x01(\t"\xa6\x02\n\x17ReportInvocationRequest\x12:\n\x0ehandler_invoke\x18\x01 \x01(\x0b2".cortex.axon.DispatchHandlerInvoke\x12:\n\x16start_client_timestamp\x18d \x01(\x0b2\x1a.google.protobuf.Timestamp\x12\x13\n\x0bduration_ms\x18e \x01(\x05\x12,\n\x06result\x18\xc8\x01 \x01(\x0b2\x19.cortex.axon.InvokeResultH\x00\x12$\n\x05error\x18\xc9\x01 \x01(\x0b2\x12.cortex.axon.ErrorH\x00\x12\x1f\n\x04logs\x18\xac\x02 \x03(\x0b2\x10.cortex.axon.LogB\t\n\x07message"=\n\x18ReportInvocationResponse\x12!\n\x05error\x18\x01 \x01(\x0b2\x12.cortex.axon.Error"\x1d\n\x0cInvokeResult\x12\r\n\x05value\x18\n \x01(\t"\xb2\x01\n\x18GetHandlerHistoryRequest\x12\x14\n\x0chandler_name\x18\x01 \x01(\t\x12.\n\nstart_time\x18\x02 \x01(\x0b2\x1a.google.protobuf.Timestamp\x12,\n\x08end_time\x18\x03 \x01(\x0b2\x1a.google.protobuf.Timestamp\x12\x14\n\x0cinclude_logs\x18\x04 \x01(\x08\x12\x0c\n\x04tail\x18\x05 \x01(\x05"\xf8\x02\n\x10HandlerExecution\x12\x14\n\x0chandler_name\x18\x01 \x01(\t\x12\x12\n\nhandler_id\x18\x02 \x01(\t\x12\x15\n\rinvocation_id\x18\x03 \x01(\t\x12\x13\n\x0bdispatch_id\x18\x04 \x01(\t\x12<\n\x18publish_server_timestamp\x18\n \x01(\x0b2\x1a.google.protobuf.Timestamp\x12<\n\x18receive_server_timestamp\x18\x0b \x01(\x0b2\x1a.google.protobuf.Timestamp\x12:\n\x16start_client_timestamp\x18\x0c \x01(\x0b2\x1a.google.protobuf.Timestamp\x12\x13\n\x0bduration_ms\x18\r \x01(\x05\x12!\n\x05error\x18\x14 \x01(\x0b2\x12.cortex.axon.Error\x12\x1e\n\x04logs\x18\x1e \x03(\x0b2\x10.cortex.axon.Log"n\n\x19GetHandlerHistoryResponse\x12!\n\x05error\x18\x01 \x01(\x0b2\x12.cortex.axon.Error\x12.\n\x07history\x18\x02 \x03(\x0b2\x1d.cortex.axon.HandlerExecution*^\n\x11HandlerInvokeType\x12\n\n\x06INVOKE\x10\x00\x12\x0b\n\x07RUN_NOW\x10\x01\x12\x11\n\rCRON_SCHEDULE\x10\x02\x12\x10\n\x0cRUN_INTERVAL\x10\x03\x12\x0b\n\x07WEBHOOK\x10\x04*w\n\x13DispatchMessageType\x12\x1e\n\x1aDISPATCH_MESSAGE_TYPE_NONE\x10\x00\x12\x1b\n\x17DISPATCH_MESSAGE_INVOKE\x10\x01\x12#\n\x1fDISPATCH_MESSAGE_WORK_COMPLETED\x10\x022\xb3\x04\n\tAxonAgent\x12\\\n\x0fRegisterHandler\x12#.cortex.axon.RegisterHandlerRequest\x1a$.cortex.axon.RegisterHandlerResponse\x12b\n\x11UnregisterHandler\x12%.cortex.axon.UnregisterHandlerRequest\x1a&.cortex.axon.UnregisterHandlerResponse\x12S\n\x0cListHandlers\x12 .cortex.axon.ListHandlersRequest\x1a!.cortex.axon.ListHandlersResponse\x12b\n\x11GetHandlerHistory\x12%.cortex.axon.GetHandlerHistoryRequest\x1a&.cortex.axon.GetHandlerHistoryResponse\x12J\n\x08Dispatch\x12\x1c.cortex.axon.DispatchRequest\x1a\x1c.cortex.axon.DispatchMessage(\x010\x01\x12_\n\x10ReportInvocation\x12$.cortex.axon.ReportInvocationRequest\x1a%.cortex.axon.ReportInvocationResponseB\x1cZ\x1agithub.com/cortexapps/axonb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cortex_axon_agent_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'Z\x1agithub.com/cortexapps/axon'
    _globals['_DISPATCHHANDLERINVOKE_ARGSENTRY']._loaded_options = None
    _globals['_DISPATCHHANDLERINVOKE_ARGSENTRY']._serialized_options = b'8\x01'
    _globals['_HANDLERINVOKETYPE']._serialized_start = 2514
    _globals['_HANDLERINVOKETYPE']._serialized_end = 2608
    _globals['_DISPATCHMESSAGETYPE']._serialized_start = 2610
    _globals['_DISPATCHMESSAGETYPE']._serialized_end = 2729
    _globals['_REGISTERHANDLERREQUEST']._serialized_start = 88
    _globals['_REGISTERHANDLERREQUEST']._serialized_end = 220
    _globals['_HANDLERINVOKEOPTION']._serialized_start = 222
    _globals['_HANDLERINVOKEOPTION']._serialized_end = 304
    _globals['_HANDLEROPTION']._serialized_start = 306
    _globals['_HANDLEROPTION']._serialized_end = 383
    _globals['_REGISTERHANDLERRESPONSE']._serialized_start = 385
    _globals['_REGISTERHANDLERRESPONSE']._serialized_end = 457
    _globals['_UNREGISTERHANDLERREQUEST']._serialized_start = 459
    _globals['_UNREGISTERHANDLERREQUEST']._serialized_end = 497
    _globals['_UNREGISTERHANDLERRESPONSE']._serialized_start = 499
    _globals['_UNREGISTERHANDLERRESPONSE']._serialized_end = 561
    _globals['_LISTHANDLERSREQUEST']._serialized_start = 563
    _globals['_LISTHANDLERSREQUEST']._serialized_end = 584
    _globals['_HANDLERINFO']._serialized_start = 587
    _globals['_HANDLERINFO']._serialized_end = 778
    _globals['_LISTHANDLERSRESPONSE']._serialized_start = 780
    _globals['_LISTHANDLERSRESPONSE']._serialized_end = 881
    _globals['_DISPATCHREQUEST']._serialized_start = 883
    _globals['_DISPATCHREQUEST']._serialized_end = 945
    _globals['_DISPATCHMESSAGE']._serialized_start = 948
    _globals['_DISPATCHMESSAGE']._serialized_end = 1078
    _globals['_DISPATCHHANDLERINVOKE']._serialized_start = 1081
    _globals['_DISPATCHHANDLERINVOKE']._serialized_end = 1363
    _globals['_DISPATCHHANDLERINVOKE_ARGSENTRY']._serialized_start = 1320
    _globals['_DISPATCHHANDLERINVOKE_ARGSENTRY']._serialized_end = 1363
    _globals['_LOG']._serialized_start = 1365
    _globals['_LOG']._serialized_end = 1449
    _globals['_REPORTINVOCATIONREQUEST']._serialized_start = 1452
    _globals['_REPORTINVOCATIONREQUEST']._serialized_end = 1746
    _globals['_REPORTINVOCATIONRESPONSE']._serialized_start = 1748
    _globals['_REPORTINVOCATIONRESPONSE']._serialized_end = 1809
    _globals['_INVOKERESULT']._serialized_start = 1811
    _globals['_INVOKERESULT']._serialized_end = 1840
    _globals['_GETHANDLERHISTORYREQUEST']._serialized_start = 1843
    _globals['_GETHANDLERHISTORYREQUEST']._serialized_end = 2021
    _globals['_HANDLEREXECUTION']._serialized_start = 2024
    _globals['_HANDLEREXECUTION']._serialized_end = 2400
    _globals['_GETHANDLERHISTORYRESPONSE']._serialized_start = 2402
    _globals['_GETHANDLERHISTORYRESPONSE']._serialized_end = 2512
    _globals['_AXONAGENT']._serialized_start = 2732
    _globals['_AXONAGENT']._serialized_end = 3295