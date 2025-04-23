"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 28, 1, '', 'cortex-api.proto')
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10cortex-api.proto\x12\x0bcortex.axon"O\n\x0bCallRequest\x12\x0e\n\x06method\x18\x02 \x01(\t\x12\x0c\n\x04path\x18\x03 \x01(\t\x12\x14\n\x0ccontent_type\x18\x04 \x01(\t\x12\x0c\n\x04body\x18\x05 \x01(\t"\xaa\x01\n\x0cCallResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\x05\x12\x0e\n\x06status\x18\x02 \x01(\t\x127\n\x07headers\x18\x03 \x03(\x0b2&.cortex.axon.CallResponse.HeadersEntry\x12\x0c\n\x04body\x18\x04 \x01(\t\x1a.\n\x0cHeadersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x028\x012H\n\tCortexApi\x12;\n\x04Call\x12\x18.cortex.axon.CallRequest\x1a\x19.cortex.axon.CallResponseB\x1cZ\x1agithub.com/cortexapps/axonb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cortex_api_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'Z\x1agithub.com/cortexapps/axon'
    _globals['_CALLRESPONSE_HEADERSENTRY']._loaded_options = None
    _globals['_CALLRESPONSE_HEADERSENTRY']._serialized_options = b'8\x01'
    _globals['_CALLREQUEST']._serialized_start = 33
    _globals['_CALLREQUEST']._serialized_end = 112
    _globals['_CALLRESPONSE']._serialized_start = 115
    _globals['_CALLRESPONSE']._serialized_end = 285
    _globals['_CALLRESPONSE_HEADERSENTRY']._serialized_start = 239
    _globals['_CALLRESPONSE_HEADERSENTRY']._serialized_end = 285
    _globals['_CORTEXAPI']._serialized_start = 287
    _globals['_CORTEXAPI']._serialized_end = 359