import logging

from api.v1 import pb_token_system_pb2 as api_token_system_pb2
from api.v1 import pb_token_system_pb2_grpc as api_token_system_pb2_grpc
from internal.service.exception import APIExceptionHandler
from internal.biz import TokenSystemUseCase, CreateTokenReq, GetTokenReq


class TokenSystemService(api_token_system_pb2_grpc.APIServicer):
    """grpc 服务"""

    def __init__(self, token_system_use_case: TokenSystemUseCase):
        self._token_system_use_case = token_system_use_case

    @APIExceptionHandler(api_token_system_pb2.CreateTokenResp)
    def CreateToken(self, request, context):
        logging.info('CreateToken api')

        self._token_system_use_case.create_token(CreateTokenReq(
            topic=request.topic,
            bucket=request.bucket,
            token_per_second=request.tokenPerSecond
        ))

        return api_token_system_pb2.CreateTokenResp(err=api_token_system_pb2.OK)

    @APIExceptionHandler(api_token_system_pb2.StartTokenResp)
    def StartToken(self, request, context):
        logging.info('StartToken api')

        self._token_system_use_case.start_token(request.topic)

        return api_token_system_pb2.StartTokenResp(err=api_token_system_pb2.OK)

    @APIExceptionHandler(api_token_system_pb2.GetTokenResp)
    def GetToken(self, request, context):
        logging.info('GetToken api')

        self._token_system_use_case.get_token(GetTokenReq(
            topic=request.topic,
            count=request.count
        ))

        return api_token_system_pb2.GetTokenResp(err=api_token_system_pb2.OK)

    @APIExceptionHandler(api_token_system_pb2.DeleteTokenResp)
    def DeleteToken(self, request, context):
        """"""
        logging.info('DeleteToken api')

        self._token_system_use_case.delete_token(request.topic)

        return api_token_system_pb2.DeleteTokenResp(err=api_token_system_pb2.OK)


def new_service(token_system_use_case: TokenSystemUseCase) -> TokenSystemService:
    return TokenSystemService(token_system_use_case)
