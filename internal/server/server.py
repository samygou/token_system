import typing as t

from api.v1 import pb_token_system_pb2_grpc as api_token_system_pb2_grpc
from internal.modules.grpcx import GRPCServer


def new_grpc_server(
        port: int,
        api_svc,
        workers=10,
        options: t.List[t.Tuple] = None,
        private_key: t.Optional[t.AnyStr] = None,
        certificate: t.Optional[t.AnyStr] = None
) -> GRPCServer:
    """
    gRPC实例化
    :param certificate:
    :param private_key:
    :param port:
    :param api_svc:
    :param workers:
    :param options:
    :param private_key: 私钥
    :param certificate: 证书
    :return:
    """
    return GRPCServer(
        port,
        api_svc,
        workers,
        options,
        api_token_system_pb2_grpc.add_APIServicer_to_server,
        private_key=private_key,
        certificate=certificate
    )
