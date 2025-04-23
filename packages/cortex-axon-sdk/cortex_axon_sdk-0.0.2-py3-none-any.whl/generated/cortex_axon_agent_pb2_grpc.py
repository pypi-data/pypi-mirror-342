"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings
from . import cortex_axon_agent_pb2 as cortex__axon__agent__pb2
GRPC_GENERATED_VERSION = '1.68.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False
try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True
if _version_not_supported:
    raise RuntimeError(f'The grpc package installed is at version {GRPC_VERSION},' + f' but the generated code in cortex_axon_agent_pb2_grpc.py depends on' + f' grpcio>={GRPC_GENERATED_VERSION}.' + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}' + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.')

class AxonAgentStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RegisterHandler = channel.unary_unary('/cortex.axon.AxonAgent/RegisterHandler', request_serializer=cortex__axon__agent__pb2.RegisterHandlerRequest.SerializeToString, response_deserializer=cortex__axon__agent__pb2.RegisterHandlerResponse.FromString, _registered_method=True)
        self.UnregisterHandler = channel.unary_unary('/cortex.axon.AxonAgent/UnregisterHandler', request_serializer=cortex__axon__agent__pb2.UnregisterHandlerRequest.SerializeToString, response_deserializer=cortex__axon__agent__pb2.UnregisterHandlerResponse.FromString, _registered_method=True)
        self.ListHandlers = channel.unary_unary('/cortex.axon.AxonAgent/ListHandlers', request_serializer=cortex__axon__agent__pb2.ListHandlersRequest.SerializeToString, response_deserializer=cortex__axon__agent__pb2.ListHandlersResponse.FromString, _registered_method=True)
        self.GetHandlerHistory = channel.unary_unary('/cortex.axon.AxonAgent/GetHandlerHistory', request_serializer=cortex__axon__agent__pb2.GetHandlerHistoryRequest.SerializeToString, response_deserializer=cortex__axon__agent__pb2.GetHandlerHistoryResponse.FromString, _registered_method=True)
        self.Dispatch = channel.stream_stream('/cortex.axon.AxonAgent/Dispatch', request_serializer=cortex__axon__agent__pb2.DispatchRequest.SerializeToString, response_deserializer=cortex__axon__agent__pb2.DispatchMessage.FromString, _registered_method=True)
        self.ReportInvocation = channel.unary_unary('/cortex.axon.AxonAgent/ReportInvocation', request_serializer=cortex__axon__agent__pb2.ReportInvocationRequest.SerializeToString, response_deserializer=cortex__axon__agent__pb2.ReportInvocationResponse.FromString, _registered_method=True)

class AxonAgentServicer(object):
    """Missing associated documentation comment in .proto file."""

    def RegisterHandler(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UnregisterHandler(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListHandlers(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetHandlerHistory(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Dispatch(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReportInvocation(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_AxonAgentServicer_to_server(servicer, server):
    rpc_method_handlers = {'RegisterHandler': grpc.unary_unary_rpc_method_handler(servicer.RegisterHandler, request_deserializer=cortex__axon__agent__pb2.RegisterHandlerRequest.FromString, response_serializer=cortex__axon__agent__pb2.RegisterHandlerResponse.SerializeToString), 'UnregisterHandler': grpc.unary_unary_rpc_method_handler(servicer.UnregisterHandler, request_deserializer=cortex__axon__agent__pb2.UnregisterHandlerRequest.FromString, response_serializer=cortex__axon__agent__pb2.UnregisterHandlerResponse.SerializeToString), 'ListHandlers': grpc.unary_unary_rpc_method_handler(servicer.ListHandlers, request_deserializer=cortex__axon__agent__pb2.ListHandlersRequest.FromString, response_serializer=cortex__axon__agent__pb2.ListHandlersResponse.SerializeToString), 'GetHandlerHistory': grpc.unary_unary_rpc_method_handler(servicer.GetHandlerHistory, request_deserializer=cortex__axon__agent__pb2.GetHandlerHistoryRequest.FromString, response_serializer=cortex__axon__agent__pb2.GetHandlerHistoryResponse.SerializeToString), 'Dispatch': grpc.stream_stream_rpc_method_handler(servicer.Dispatch, request_deserializer=cortex__axon__agent__pb2.DispatchRequest.FromString, response_serializer=cortex__axon__agent__pb2.DispatchMessage.SerializeToString), 'ReportInvocation': grpc.unary_unary_rpc_method_handler(servicer.ReportInvocation, request_deserializer=cortex__axon__agent__pb2.ReportInvocationRequest.FromString, response_serializer=cortex__axon__agent__pb2.ReportInvocationResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('cortex.axon.AxonAgent', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('cortex.axon.AxonAgent', rpc_method_handlers)

class AxonAgent(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def RegisterHandler(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cortex.axon.AxonAgent/RegisterHandler', cortex__axon__agent__pb2.RegisterHandlerRequest.SerializeToString, cortex__axon__agent__pb2.RegisterHandlerResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def UnregisterHandler(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cortex.axon.AxonAgent/UnregisterHandler', cortex__axon__agent__pb2.UnregisterHandlerRequest.SerializeToString, cortex__axon__agent__pb2.UnregisterHandlerResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def ListHandlers(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cortex.axon.AxonAgent/ListHandlers', cortex__axon__agent__pb2.ListHandlersRequest.SerializeToString, cortex__axon__agent__pb2.ListHandlersResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def GetHandlerHistory(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cortex.axon.AxonAgent/GetHandlerHistory', cortex__axon__agent__pb2.GetHandlerHistoryRequest.SerializeToString, cortex__axon__agent__pb2.GetHandlerHistoryResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def Dispatch(request_iterator, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/cortex.axon.AxonAgent/Dispatch', cortex__axon__agent__pb2.DispatchRequest.SerializeToString, cortex__axon__agent__pb2.DispatchMessage.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def ReportInvocation(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cortex.axon.AxonAgent/ReportInvocation', cortex__axon__agent__pb2.ReportInvocationRequest.SerializeToString, cortex__axon__agent__pb2.ReportInvocationResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)