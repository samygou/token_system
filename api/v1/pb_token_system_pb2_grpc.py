# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import pb_token_system_pb2 as pb__token__system__pb2


class APIStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateToken = channel.unary_unary(
                '/token_system.api.v1.API/CreateToken',
                request_serializer=pb__token__system__pb2.CreateTokenReq.SerializeToString,
                response_deserializer=pb__token__system__pb2.CreateTokenResp.FromString,
                )
        self.StartToken = channel.unary_unary(
                '/token_system.api.v1.API/StartToken',
                request_serializer=pb__token__system__pb2.StartTokenReq.SerializeToString,
                response_deserializer=pb__token__system__pb2.StartTokenResp.FromString,
                )
        self.GetToken = channel.unary_unary(
                '/token_system.api.v1.API/GetToken',
                request_serializer=pb__token__system__pb2.GetTokenReq.SerializeToString,
                response_deserializer=pb__token__system__pb2.GetTokenResp.FromString,
                )
        self.DeleteToken = channel.unary_unary(
                '/token_system.api.v1.API/DeleteToken',
                request_serializer=pb__token__system__pb2.DeleteTokenReq.SerializeToString,
                response_deserializer=pb__token__system__pb2.DeleteTokenResp.FromString,
                )


class APIServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateToken(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StartToken(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetToken(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteToken(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_APIServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateToken': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateToken,
                    request_deserializer=pb__token__system__pb2.CreateTokenReq.FromString,
                    response_serializer=pb__token__system__pb2.CreateTokenResp.SerializeToString,
            ),
            'StartToken': grpc.unary_unary_rpc_method_handler(
                    servicer.StartToken,
                    request_deserializer=pb__token__system__pb2.StartTokenReq.FromString,
                    response_serializer=pb__token__system__pb2.StartTokenResp.SerializeToString,
            ),
            'GetToken': grpc.unary_unary_rpc_method_handler(
                    servicer.GetToken,
                    request_deserializer=pb__token__system__pb2.GetTokenReq.FromString,
                    response_serializer=pb__token__system__pb2.GetTokenResp.SerializeToString,
            ),
            'DeleteToken': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteToken,
                    request_deserializer=pb__token__system__pb2.DeleteTokenReq.FromString,
                    response_serializer=pb__token__system__pb2.DeleteTokenResp.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'token_system.api.v1.API', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class API(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateToken(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/token_system.api.v1.API/CreateToken',
            pb__token__system__pb2.CreateTokenReq.SerializeToString,
            pb__token__system__pb2.CreateTokenResp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StartToken(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/token_system.api.v1.API/StartToken',
            pb__token__system__pb2.StartTokenReq.SerializeToString,
            pb__token__system__pb2.StartTokenResp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetToken(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/token_system.api.v1.API/GetToken',
            pb__token__system__pb2.GetTokenReq.SerializeToString,
            pb__token__system__pb2.GetTokenResp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteToken(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/token_system.api.v1.API/DeleteToken',
            pb__token__system__pb2.DeleteTokenReq.SerializeToString,
            pb__token__system__pb2.DeleteTokenResp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)