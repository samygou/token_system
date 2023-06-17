import typing as t
from concurrent import futures
import logging

import grpc


class ErrPortIsNullException(Exception):
    """port is null"""


class GRPCServer:
    """gRPC server"""

    def __init__(
            self,
            port: int,
            api_svc: object,
            workers: int,
            options: t.Optional[t.List[t.Tuple]],
            register_func: t.Callable,
            private_key: str = None,
            certificate: str = None
    ):
        """
        gRPC server
        :param port: 端口
        :param api_svc: api
        :param workers: 工作线程数
        :param options: options
        :param register_func: grpc api注册函数
        :param private_key: insecure模式的私钥
        :param certificate: 证书, 为空使用非安全模式
        """
        self._port = port
        self._options = options if options else \
            [
                ('grpc.max_send_message_length', 100 * 1024 * 1024),
                ('grpc.max_receive_message_length', 100 * 1024 * 1024)
            ]
        self._workers = workers
        self._api_svc = api_svc
        self.server = None
        self._register_func = register_func
        self._private_key = private_key
        self._certificate = certificate

    def serve(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=self._workers), options=self._options)
        self._register_func(self._api_svc, self.server)

        if not self._port:
            raise ErrPortIsNullException

        if not self._private_key or not self._certificate:
            logging.info('insecure mode')
            self.server.add_insecure_port(f'[::]:{self._port}')
        else:
            logging.info('TSL/SSL mode')
            server_credentials = grpc.ssl_server_credentials(
                ((self._private_key, self._certificate), )
            )
            self.server.add_secure_port(f'[::]:{self._port}', server_credentials)

        self.server.start()

        logging.info('start grpc serve...')
